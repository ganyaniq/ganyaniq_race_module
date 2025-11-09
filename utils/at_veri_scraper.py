import requests
from bs4 import BeautifulSoup
import time
from db.db_writer import DatabaseWriter

class AtVeriScraper:
    def __init__(self, base_url, db_writer: DatabaseWriter, delay=2):
        self.base_url = base_url
        self.db_writer = db_writer
        self.delay = delay
        self.visited_urls = set()

    def fetch_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"[!] Hata: {url} çekilemedi - {e}")
            return None

    def parse_at_list(self, html):
        soup = BeautifulSoup(html, "html.parser")
        at_links = []
        for a_tag in soup.select("a.at-link-class"):  # Güncel selector ile değiştir
            href = a_tag.get("href")
            if href and href not in self.visited_urls:
                at_links.append(href)
                self.visited_urls.add(href)
        return at_links

    def fetch_and_store_at_details(self, at_url):
        full_url = self.base_url + at_url
        html = self.fetch_page(full_url)
        if not html:
            return
        soup = BeautifulSoup(html, "html.parser")
        at_name = soup.select_one("h1.at-name").text.strip()  # Güncel selector ile değiştir
        details = {
            "name": at_name,
            # Diğer detaylar buraya
        }
        self.db_writer.write_at_details(details)
        print(f"[✓] At detayları kaydedildi: {at_name}")

    def crawl_all_ats(self, start_url):
        queue = [start_url]
        while queue:
            current_url = queue.pop(0)
            full_url = self.base_url + current_url
            html = self.fetch_page(full_url)
            if not html:
                continue
            at_links = self.parse_at_list(html)
            for at_link in at_links:
                self.fetch_and_store_at_details(at_link)
                time.sleep(self.delay)
            # Pagination eklenebilir
