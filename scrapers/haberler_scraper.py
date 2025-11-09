import requests
from bs4 import BeautifulSoup
import time
import logging
from db_writer import DBWriter

logging.basicConfig(level=logging.INFO)

class HaberlerScraper:
    def __init__(self):
        self.base_url = "https://www.ganyancanavari.com"
        self.db_writer = DBWriter()
        self.delay = 1.5

    def fetch_page(self, path):
        url = self.base_url + path
        try:
            logging.info(f"Fetching {url}")
            response = requests.get(url)
            response.raise_for_status()
            time.sleep(self.delay)
            return response.text
        except Exception as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return None

    def parse_and_save(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        haberler = []
        for haber_div in soup.select('.manset-haber'):
            try:
                title = haber_div.select_one('.haber-baslik').text.strip()
                link = haber_div.select_one('a')['href']
                summary = haber_div.select_one('.haber-ozet').text.strip()
                haberler.append({
                    'title': title,
                    'link': link,
                    'summary': summary
                })
            except Exception as e:
                logging.error(f"Parse error: {e}")
        if haberler:
            self.db_writer.insert_haberler(haberler)
            logging.info(f"{len(haberler)} haber kaydedildi.")

    def scrape(self):
        html = self.fetch_page("/site/haberler.html")
        if html:
            self.parse_and_save(html)
        else:
            logging.warning("Haberler sayfası çekilemedi.")

    def close(self):
        self.db_writer.close()

if __name__ == "__main__":
    scraper = HaberlerScraper()
    scraper.scrape()
    scraper.close()
