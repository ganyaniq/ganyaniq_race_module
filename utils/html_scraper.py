import requests
from bs4 import BeautifulSoup
import datetime
import os

class HTMLScraper:
    def __init__(self, base_url, output_dir="data/html_cache"):
        self.base_url = base_url
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_and_save(self, endpoint="", date_format="%Y-%m-%d"):
        """
        Belirli bir endpoint'ten HTML verisini çekip dosyaya kaydeder.
        """
        today = datetime.datetime.today().strftime(date_format)
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url
        response = requests.get(url)

        if response.status_code == 200:
            filename = f"{self.output_dir}/page_{today}.html"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"[✓] HTML başarıyla kaydedildi: {filename}")
            return filename
        else:
            print(f"[!] Hata: {url} erişilemedi. Kod: {response.status_code}")
            return None

    def parse_table(self, html_file, table_index=0):
        """
        Kaydedilen HTML dosyasından tablo verisini çıkarır.
        """
        with open(html_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            tables = soup.find_all("table")
            if tables and len(tables) > table_index:
                return tables[table_index]
            else:
                print("[!] Tablo bulunamadı.")
                return None

# Örnek kullanım:
# scraper = HTMLScraper("https://example.com/program")
# html_file = scraper.fetch_and_save()
# table = scraper.parse_table(html_file)
