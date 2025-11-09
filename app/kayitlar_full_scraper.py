# app/kayitlar_full_scraper.py
import requests
from bs4 import BeautifulSoup
from time import sleep
from db_utils import get_db_connection

BASE_URL = "https://www.ganyancanavari.com/site/kayitlar.html"

def fetch_kayitlar_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; GanyanIQBot/1.0)"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def parse_kayitlar_list(soup):
    kayitlar = []
    kayit_table = soup.find("table", {"id": "kayitlarTable"})
    if kayit_table:
        rows = kayit_table.find_all("tr")[1:]  # Header hariç
        for row in rows:
            cols = row.find_all("td")
            kayit = {
                "kayit_id": cols[0].text.strip(),
                "at_adi": cols[1].text.strip(),
                "tarih": cols[2].text.strip(),
                # Diğer sütunlar eklenmeli
            }
            kayitlar.append(kayit)
    return kayitlar

def fetch_all_kayitlar():
    kayitlar_tumu = []
    next_page_url = BASE_URL

    while next_page_url:
        soup = fetch_kayitlar_page(next_page_url)
        kayitlar = parse_kayitlar_list(soup)
        kayitlar_tumu.extend(kayitlar)

        next_link = soup.find("a", {"class": "next"})
        if next_link and 'href' in next_link.attrs:
            next_page_url = next_link['href']
            sleep(2)
        else:
            next_page_url = None

    return kayitlar_tumu

def write_kayitlar_to_db(kayitlar):
    conn = get_db_connection()
    cur = conn.cursor()
    for kayit in kayitlar:
        cur.execute("""
            INSERT INTO kayitlar (kayit_id, at_adi, tarih)
            VALUES (%s, %s, %s)
            ON CONFLICT (kayit_id) DO UPDATE SET at_adi = EXCLUDED.at_adi, tarih = EXCLUDED.tarih;
        """, (kayit['kayit_id'], kayit['at_adi'], kayit['tarih']))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    kayitlar = fetch_all_kayitlar()
    write_kayitlar_to_db(kayitlar)
