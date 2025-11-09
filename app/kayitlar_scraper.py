# app/kayitlar_scraper.py
import requests
from bs4 import BeautifulSoup
from db_utils import get_db_connection

def fetch_kayitlar():
    url = "https://www.ganyancanavari.com/site/kayitlar.html"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    kayitlar_list = []
    # Alt sayfalar varsa onlar da çekilecek, tüm at ve kayıt detayları çıkarılacak.

    # TODO: Detaylı parsing kodu buraya eklenecek

    return kayitlar_list

def write_kayitlar_to_db(kayitlar_list):
    conn = get_db_connection()
    cur = conn.cursor()
    for kayit in kayitlar_list:
        cur.execute("""
            INSERT INTO kayitlar (kayit_id, at_adi, tarih, ...)
            VALUES (%s, %s, %s, ...)
            ON CONFLICT (kayit_id) DO UPDATE SET at_adi = EXCLUDED.at_adi;
        """, (kayit['kayit_id'], kayit['at_adi'], kayit['tarih']))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    kayitlar = fetch_kayitlar()
    write_kayitlar_to_db(kayitlar)
