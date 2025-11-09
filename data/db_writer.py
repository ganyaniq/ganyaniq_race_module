import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "dbname": os.getenv("DB_NAME")
}

def veri_yaz(json_dosya_yolu, tablo_adi):
    try:
        with open(json_dosya_yolu, "r", encoding="utf-8") as f:
            veri_listesi = json.load(f)

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for veri in veri_listesi:
            kolonlar = ', '.join(veri.keys())
            degerler = ', '.join([f'%({k})s' for k in veri.keys()])
            sorgu = f"INSERT INTO {tablo_adi} ({kolonlar}) VALUES ({degerler}) ON CONFLICT DO NOTHING"
            cur.execute(sorgu, veri)

        conn.commit()
        cur.close()
        conn.close()
        print(f"[✓] {json_dosya_yolu} -> {tablo_adi} aktarımı tamamlandı.")

    except Exception as e:
        print(f"[HATA] {json_dosya_yolu} aktarımında sorun: {e}")
