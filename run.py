# ganyaniq_race_module/run.py

import logging
from datetime import datetime

from utils.html_scraper import HTMLScraper
from utils.csv_loader import load_csv_to_db
from ai_training.train_alfonso import start_training
from analizler.lyra_grafik_modulu import grafik_tahmin_performansi
from ai_training.tahmin_motoru import TahminMotoru
from db.database import SessionLocal
from db.db_writer import DatabaseWriter

logging.basicConfig(
    filename="ganyaniq_run.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def main():
    logging.info("GANYAN IQ RUN started")

    try:
        # 1. Veri çek ve işleme (örnek url)
        scraper = HTMLScraper("https://www.tjk.org/")
        html_file = scraper.fetch_and_save()

        # 2. CSV'leri veritabanına aktar
        load_csv_to_db("data/csv")

        # 3. AI eğitimini başlat
        start_training()

        # 4. LYRA grafik analizini üret
        grafik_tahmin_performansi()

        # 5. Alfonso tahmin motorunu çalıştır
        db = SessionLocal()
        tahmin_motoru = TahminMotoru(db)
        tahmin_motoru.tum_kosular_icin_tahmin_yap()

        logging.info("GANYAN IQ RUN finished successfully")
    except Exception as e:
        logging.error(f"Error during GANYAN IQ RUN: {e}")

if __name__ == "__main__":
    main()
