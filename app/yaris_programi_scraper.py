# yaris_programi_scraper.py
import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

def fetch_daily_program():
    url = "https://www.tjk.org/TR/YarisSever/Program/Index"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    program_list = []
    # Parse HTML and extract race info logic here...
    
    return program_list

def write_to_db(program_list):
    conn = psycopg2.connect(dbname="yaris_veritabani", user="max_user", password="r6P54e4ViGiYlVx7rkwLskmQhq830NN8Y", host="dpg-cvits1ali9vc73djuurg-a", port=5432)
    cur = conn.cursor()
    for race in program_list:
        cur.execute("""
            INSERT INTO yaris_programi (race_date, race_time, hipodrom, kosu_sayisi, ...)
            VALUES (%s, %s, %s, %s, ...)
            ON CONFLICT (race_date, race_time, hipodrom) DO UPDATE SET kosu_sayisi = EXCLUDED.kosu_sayisi;
        """, (race['date'], race['time'], race['hipodrom'], race['kosu_sayisi']))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    program = fetch_daily_program()
    write_to_db(program)
