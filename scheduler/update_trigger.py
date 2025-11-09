from scrapers.kategori_scraper import fetch_kategori_data
from db.db_writer import write_to_db
from loggers.update_logger import log_update
from loggers.error_handler import handle_error

CATEGORY_URLS = [
    "https://www.example.com/kategori1",
    "https://www.example.com/kategori2",
    # Tüm kategori URL’leri buraya eklenecek
]

def trigger_updates():
    log_update("Güncelleme tetiklendi.")
    for url in CATEGORY_URLS:
        try:
            data = fetch_kategori_data(url)
            write_to_db(data)
            log_update(f"{url} verisi güncellendi.")
        except Exception as e:
            handle_error(e)
            log_update(f"{url} güncelleme sırasında hata oluştu.")
