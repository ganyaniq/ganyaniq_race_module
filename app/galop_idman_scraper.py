# app/galop_idman_scraper.py
import requests
from bs4 import BeautifulSoup
from db_utils import get_db_connection

def fetch_galoplar():
    url = "https://www.ganyancanavari.com/site/gunluk-galoplar.html"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    galop_list = []
    # Galop verileri parsing yapılacak

    # TODO: Detaylar eklenecek

    return galop_list

def write_galoplar_to_db(galop_list):
    conn = get_db_connection()
    cur = conn.cursor()
    for galop in galop_list:
        cur.execute("""
            INSERT INTO galoplar (id, at_adi, tarih, performans, ...)
            VALUES (%s, %s, %s, %s, ...)
            ON CONFLICT (id) DO UPDATE SET performans = EXCLUDED.performans;
        """, (galop['id'], galop['at_adi'], galop['tarih'], galop['performans']))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    galoplar = fetch_galoplar()
    write_galoplar_to_db(galoplar)
