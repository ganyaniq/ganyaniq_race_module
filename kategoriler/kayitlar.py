import requests
from db.content_parser import parse_table
from db.db_writer import DBWriter

def fetch_kayitlar():
    url = "https://www.ganyancanavari.com/site/kayitlar.html"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; GANYANIQBot/1.0)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching kayitlar: {e}")
        return ""

def main():
    html_content = fetch_kayitlar()
    if not html_content:
        return

    all_tables_data = parse_table(html_content)
    
    db_params = {
        "dbname": "yaris_veritabani",
        "user": "max_user",
        "password": "r6P54e4ViGiYlVx7rkwLskmQhq830NN8Y",
        "host": "dpg-cvits1ali9vc73djuurg-a",
        "port": 5432
    }
    writer = DBWriter(db_params)

    for table_data in all_tables_data:
        writer.save_records('kayitlar', table_data)

    writer.close()

if __name__ == "__main__":
    main()
