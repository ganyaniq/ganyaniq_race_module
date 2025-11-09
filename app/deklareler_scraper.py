# app/deklareler_scraper.py
import requests
from bs4 import BeautifulSoup
from db_utils import get_db_connection

def fetch_deklareler():
    url = "https://www.ganyancanavari.com/site/deklareler.html"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    deklare_list = []
    # Burada alt sayfalar varsa onları da çekme kodu olacak.
    # Örnek: Sayfadaki ilanları, at bilgilerini çıkarma.

    # TODO: Detaylı parsing kodu eklenecek

    return deklare_list

def write_deklareler_to_db(deklare_list):
    conn = get_db_connection()
    cur = conn.cursor()
    for deklare in deklare_list:
        cur.execute("""
            INSERT INTO deklareler (ilan_id, at_adi, tarih, ...)
            VALUES (%s, %s, %s, ...)
            ON CONFLICT (ilan_id) DO UPDATE SET at_adi = EXCLUDED.at_adi;
        """, (deklare['ilan_id'], deklare['at_adi'], deklare['tarih']))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    deklareler = fetch_deklareler()
    write_deklareler_to_db(deklareler)
