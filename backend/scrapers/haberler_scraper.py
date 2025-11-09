from scraper_base import ScraperBase
from db_writer import DBWriter
import logging

class HaberlerScraper(ScraperBase):
    def __init__(self):
        super().__init__(base_url="https://www.ganyancanavari.com")

    def parse(self, html: str):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        haberler = []

        # Örnek: Manşet haberler div içinde çekilecek
        manşetler = soup.select('.manset-haber')  # CSS selector güncellenmeli
        for haber in manşetler:
            title = haber.select_one('.haber-baslik').text.strip()
            link = haber.select_one('a')['href']
            summary = haber.select_one('.haber-ozet').text.strip()
            haberler.append({
                'title': title,
                'link': link,
                'summary': summary,
            })
        return haberler

def run_haberler_scraper():
    scraper = HaberlerScraper()
    db_writer = DBWriter()
    try:
        haberler = scraper.scrape('/site/haberler.html')
        if haberler:
            # DB kaydı yapılacak (tablo ve insert metodu örnek)
            db_writer.insert_haberler(haberler)
            logging.info(f"{len(haberler)} haber kaydedildi.")
        else:
            logging.warning("Haberler çekilemedi.")
    finally:
        db_writer.close()

if __name__ == "__main__":
    run_haberler_scraper()
