import requests
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO)

class ScraperBase:
    def __init__(self, base_url: str, headers=None, delay=1.0):
        self.base_url = base_url
        self.headers = headers or {'User-Agent': 'Mozilla/5.0'}
        self.delay = delay

    def fetch(self, url: str):
        logging.info(f"Fetching URL: {url}")
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            time.sleep(self.delay)  # Ban yememek için delay
            return response.text
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            return None

    def parse(self, html: str):
        # Override edilecek
        raise NotImplementedError

    def scrape(self, path: str):
        url = self.base_url + path
        html = self.fetch(url)
        if html:
            return self.parse(html)
        return None
