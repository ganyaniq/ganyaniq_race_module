import schedule
import time
from update_trigger import trigger_updates

def run_scheduler():
    # Kategoriler ve güncelleme frekanslarına göre görevler ayarlanmalı
    schedule.every(3).minutes.do(trigger_updates)  # Örnek; gerçek zamanlama kategorilere göre düzenlenecek
    schedule.every().hour.do(trigger_updates)
    schedule.every().day.at("03:00").do(trigger_updates)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
