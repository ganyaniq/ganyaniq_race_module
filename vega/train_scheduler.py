
import schedule
import time
import subprocess
from datetime import datetime

def alfonso_egitimi():
    print(f"[{datetime.now()}] Alfonso AI eğitimi başlatılıyor...")
    subprocess.call(["python", "ai_training/train_alfonso.py"])

# Günlük sabah 06:00'da
schedule.every().day.at("06:00").do(alfonso_egitimi)

# Yarış öncesi saatlerde (örnek saatler)
for saat in ["09:00", "11:00", "13:00", "15:00"]:
    schedule.every().day.at(saat).do(alfonso_egitimi)

def scheduler_baslat():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    scheduler_baslat()
