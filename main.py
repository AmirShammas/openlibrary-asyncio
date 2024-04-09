import asyncio
import aiohttp
from bs4 import BeautifulSoup
from handler import ResultHandler, ScraperHandler
from constants import SEARCH_PAGE_COUNT, SEARCH_SUBJECT


if __name__ == "__main__":
    try:
        URL_TEMPLATE = "https://openlibrary.org/search?q={search_subject}&page={page_number}"

        async def fetch_page(session, url):
            async with session.get(url) as response:
                return await response.text()

        async def scrape_page(search_subject, page_number):
            url = URL_TEMPLATE.format(
                search_subject=search_subject, page_number=page_number)
            async with aiohttp.ClientSession() as session:
                html = await fetch_page(session, url)
                soup = BeautifulSoup(html, "html.parser")
                book_titles, book_urls = ScraperHandler.get_book_title(soup)
                authors_names, authors_urls = ScraperHandler.get_book_author(
                    soup)
                book_covers = ScraperHandler.get_book_cover(soup)
                ResultHandler.save_to_csv(
                    book_titles, book_urls, authors_names, authors_urls, book_covers)

        async def scrape_pages():
            tasks = []
            search_subject = input("Search Subject (default = music) : ") or SEARCH_SUBJECT
            search_page_count = int(
                input("Search Page Count (default = 1) : ") or SEARCH_PAGE_COUNT)
            print("Scraping ...! Please wait ...!")
            for page_number in range(1, search_page_count + 1):
                task = asyncio.create_task(
                    scrape_page(search_subject, page_number))
                tasks.append(task)
            await asyncio.gather(*tasks)
            print("Done !!")

        asyncio.run(scrape_pages())

    except Exception as error:
        print("ERROR !!")
    finally:
        print("END !!")
