import asyncio
from playwright.async_api import async_playwright
from db.db_writer import DBWriter
from db.content_parser import parse_table

db_params = {
    "dbname": "yaris_veritabani",
    "user": "max_user",
    "password": "r6P54e4ViGiYlVx7rkwLskmQhq830NN8Y",
    "host": "dpg-cvits1ali9vc73djuurg-a",
    "port": 5432
}

async def fetch_sorgulamalar(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content

async def main():
    url = "https://www.ganyancanavari.com/site/sorgulamalar.html"
    html_content = await fetch_sorgulamalar(url)

    tables_data = parse_table(html_content)
    writer = DBWriter(db_params)
    for table_data in tables_data:
        writer.save_records("sorgulamalar", table_data)
    writer.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
