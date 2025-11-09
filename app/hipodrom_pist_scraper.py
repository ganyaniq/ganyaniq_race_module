# app/hipodrom_pist_scraper.py
import requests
from bs4 import BeautifulSoup
from db_utils import get_db_connection

def fetch_hipodrom_pist():
    url = "https://www.tjk.org/TR/YarisSever/Query/Page/PistBilgileri"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    pist_list = []
    # Pist bilgileri ve hipodrom detayları parsing yapılacak

    # TODO: Parsing detayları eklenecek

    return pist_list

def write_hipodrom_pist_to_db(pist_list):
    conn = get_db_connection()
    cur = conn.cursor()
    for pist in pist_list:
        cur.execute("""
            INSERT INTO hipodrom_pist (pist_id, isim, durum, ...)
            VALUES (%s, %s, %s, ...)
            ON CONFLICT (pist_id) DO UPDATE SET durum = EXCLUDED.durum;
        """, (pist['pist_id'], pist['isim'], pist['durum']))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    pistler = fetch_hipodrom_pist()
    write_hipodrom_pist_to_db(pistler)
