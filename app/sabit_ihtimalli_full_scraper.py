# app/sabit_ihtimalli_full_scraper.py
import requests
from db_utils import get_db_connection

URL = "https://www.tjk.org/TR/YarisSever/Info/SabitIhtimalliOyunProgrami"

def fetch_sabit_ihtimalli():
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; GanyanIQBot/1.0)"
    }
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    data = response.json()  # JSON formatında veri

    sabit_program = []
    for item in data.get("Program", []):
        sabit_program.append({
            "id": item.get("Id"),
            "kosu_no": item.get("KosuNo"),
            "hipodrom": item.get("Hipodrom"),
            "saat": item.get("Saat"),
            "oyun_tipi": item.get("OyunTipi"),
            "program_detay": item.get("ProgramDetay")
        })

    return sabit_program

def write_sabit_ihtimalli_to_db(program_list):
    conn = get_db_connection()
    cur = conn.cursor()
    for item in program_list:
        cur.execute("""
            INSERT INTO sabit_ihtimalli (id, kosu_no, hipodrom, saat, oyun_tipi, program_detay)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                kosu_no = EXCLUDED.kosu_no,
                hipodrom = EXCLUDED.hipodrom,
                saat = EXCLUDED.saat,
                oyun_tipi = EXCLUDED.oyun_tipi,
                program_detay = EXCLUDED.program_detay;
        """, (item['id'], item['kosu_no'], item['hipodrom'], item['saat'], item['oyun_tipi'], item['program_detay']))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    program = fetch_sabit_ihtimalli()
    write_sabit_ihtimalli_to_db(program)
