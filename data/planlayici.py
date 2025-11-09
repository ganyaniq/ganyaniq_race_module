
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import csv
from tahmin_motoru import alfonso_ai_tahmin_et

def oku_yaris_saatleri(dosya="data/yaris_programi.csv"):
    saatler = []
    with open(dosya, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                tarih_str = row["tarih"]
                saat_str = row["saat"]
                dt = datetime.strptime(f"{tarih_str} {saat_str}", "%Y-%m-%d %H:%M")
                dt = dt.replace(tzinfo=ZoneInfo("Europe/Istanbul"))
                saatler.append(dt)
            except:
                continue
    return saatler

def calistir():
    tetik_zamanlari = set()
    while True:
        simdi = datetime.now(ZoneInfo("Europe/Istanbul")).replace(second=0, microsecond=0)
        saatler = oku_yaris_saatleri()

        for yaris_saati in saatler:
            for fark in [12, 4, 2, 1]:
                tetik_zaman = yaris_saati - timedelta(hours=fark)
                if tetik_zaman == simdi and tetik_zaman not in tetik_zamanlari:
                    print(f"[•] Alfonso tetikleniyor - {fark} saat öncesi")
                    alfonso_ai_tahmin_et(kaynak=f"{fark} saat önce")
                    tetik_zamanlari.add(tetik_zaman)

        time.sleep(60)

if __name__ == "__main__":
    calistir()
