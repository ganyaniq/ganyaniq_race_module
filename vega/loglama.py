
from datetime import datetime

LOG_FILE = "ganyaniq_log.txt"

def log_yaz(mesaj: str):
    zaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tam_mesaj = f"[{zaman}] {mesaj}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(tam_mesaj)
    print(tam_mesaj.strip())

# Örnek kullanım:
if __name__ == "__main__":
    log_yaz("Sistem başlatıldı.")
