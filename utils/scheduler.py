import schedule
import time
from utils.at_veri_scraper import AtVeriScraper
from db.db_writer import DatabaseWriter
from db.database import SessionLocal

def job():
    print("[*] Veri çekme ve güncelleme işi başladı.")
    db_session = SessionLocal()
    db_writer = DatabaseWriter(db_session)
    scraper = AtVeriScraper("https://www.ganyancanavari.com", db_writer)
    scraper.crawl_all_ats("/site/atlar.html")
    print("[*] Veri güncelleme işi tamamlandı.")

schedule.every(90).seconds.do(job)  # 1.5 dakikada bir

def run_scheduler():
    print("[*] Scheduler başladı.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
