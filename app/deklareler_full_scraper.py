# app/deklareler_full_scraper.py
import requests
from bs4 import BeautifulSoup
from time import sleep
from db_utils import get_db_connection

BASE_URL = "https://www.ganyancanavari.com/site/deklareler.html"

def fetch_deklareler_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; GanyanIQBot/1.0)"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def parse_deklareler_list(soup):
    ilanlar = []
    ilan_table = soup.find("table", {"id": "ilanlarTable"})
    if ilan_table:
        rows = ilan_table.find_all("tr")[1:]  # Header hariç
        for row in rows:
            cols = row.find_all("td")
            ilan = {
                "ilan_id": cols[0].text.strip(),
                "at_adi": cols[1].text.strip(),
                "tarih": cols[2].text.strip(),
                # Diğer gerekli sütunlar burada eklenmeli
            }
            ilanlar.append(ilan)
    return ilanlar

def fetch_all_deklareler():
    ilanlar_tumu = []
    next_page_url = BASE_URL

    while next_page_url:
        soup = fetch_deklareler_page(next_page_url)
        ilanlar = parse_deklareler_list(soup)
        ilanlar_tumu.extend(ilanlar)

        next_link = soup.find("a", {"class": "next"})
        if next_link and 'href' in next_link.attrs:
            next_page_url = next_link['href']
            sleep(2)  # Ban riski için bekleme
        else:
            next_page_url = None

    return ilanlar_tumu

def write_deklareler_to_db(ilanlar):
    conn = get_db_connection()
    cur = conn.cursor()
    for ilan in ilanlar:
        cur.execute("""
            INSERT INTO deklareler (ilan_id, at_adi, tarih)
            VALUES (%s, %s, %s)
            ON CONFLICT (ilan_id) DO UPDATE SET at_adi = EXCLUDED.at_adi, tarih = EXCLUDED.tarih;
        """, (ilan['ilan_id'], ilan['at_adi'], ilan['tarih']))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    ilanlar = fetch_all_deklareler()
    write_deklareler_to_db(ilanlar)
