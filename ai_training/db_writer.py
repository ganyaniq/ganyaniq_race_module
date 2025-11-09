import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import os
from dotenv import load_dotenv

load_dotenv()

# Ortam değişkenleri
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def db_baglan():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def veri_yaz(df: pd.DataFrame, tablo: str):
    print(f"📝 Veriler {tablo} tablosuna yazılıyor...")
    conn = db_baglan()
    cur = conn.cursor()

    kolonlar = list(df.columns)
    kolon_str = ", ".join(kolonlar)
    values_str = ", ".join(["%s"] * len(kolonlar))

    sql = f"INSERT INTO {tablo} ({kolon_str}) VALUES ({values_str})"

    execute_batch(cur, sql, df.values.tolist(), page_size=100)
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ {len(df)} satır başarıyla yazıldı → {tablo}")

# Örnek kullanım
if __name__ == "__main__":
    df = pd.read_csv("data/train_set.csv")
    veri_yaz(df, "ai_egitim_verisi")
