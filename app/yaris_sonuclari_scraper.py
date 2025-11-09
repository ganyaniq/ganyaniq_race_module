# yaris_sonuclari_scraper.py
import requests
from bs4 import BeautifulSoup
import psycopg2

def fetch_race_results(date):
    url = f"https://www.tjk.org/TR/YarisSever/Sonuclar/Index/{date.strftime('%Y-%m-%d')}"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    results = []
    # Parse results logic here...
    
    return results

def write_results_to_db(results):
    conn = psycopg2.connect(dbname="yaris_veritabani", user="max_user", password="r6P54e4ViGiYlVx7rkwLskmQhq830NN8Y", host="dpg-cvits1ali9vc73djuurg-a", port=5432)
    cur = conn.cursor()
    for result in results:
        cur.execute("""
            INSERT INTO yaris_sonuclari (race_id, at_adi, derece, jokey, ...)
            VALUES (%s, %s, %s, %s, ...)
            ON CONFLICT (race_id, at_adi) DO UPDATE SET derece = EXCLUDED.derece;
        """, (result['race_id'], result['at_adi'], result['derece'], result['jokey']))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    from datetime import datetime
    results = fetch_race_results(datetime.today())
    write_results_to_db(results)
