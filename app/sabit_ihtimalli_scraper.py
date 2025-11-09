# app/sabit_ihtimalli_scraper.py
import requests
from db_utils import get_db_connection

def fetch_sabit_ihtimalli():
    url = "https://www.tjk.org/TR/YarisSever/Info/SabitIhtimalliOyunProgrami"
    headers = {
        # Ban yememek için gerekli headers veya cookies eklenebilir
        "User-Agent": "Mozilla/5.0 (compatible; GanyanIQBot/1.0)"
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    data = resp.json()  # Eğer JSON formatındaysa
    # Yoksa uygun parsing yapılacak

    sabit_list = []
    # TODO: JSON parsing veya HTML parsing burada olacak

    return sabit_list

def write_sabit_to_db(sabit_list):
    conn = get_db_connection()
    cur = conn.cursor()
    for item in sabit_list:
        cur.execute("""
            INSERT INTO sabit_ihtimalli (id, program_detay, ...)
            VALUES (%s, %s, ...)
            ON CONFLICT (id) DO UPDATE SET program_detay = EXCLUDED.program_detay;
        """, (item['id'], item['program_detay']))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    sabit = fetch_sabit_ihtimalli()
    write_sabit_to_db(sabit)
