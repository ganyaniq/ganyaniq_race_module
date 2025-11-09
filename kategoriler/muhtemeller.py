import requests
from db.content_parser import parse_table
from db.db_writer import DBWriter

def fetch_muhtemeller():
    url = "https://vhs.tjk.org/muhtemeller/?hipodromkey=ANKARA"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; GANYANIQBot/1.0)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching muhtemeller: {e}")
        return ""

def main():
    html_content = fetch_muhtemeller()
    if not html_content:
        return

    tables_data = parse_table(html_content)

    db_params = {
        "dbname": "yaris_veritabani",
        "user": "max_user",
        "password": "r6P54e4ViGiYlVx7rkwLskmQhq830NN8Y",
        "host": "dpg-cvits1ali9vc73djuurg-a",
        "port": 5432
    }
    writer = DBWriter(db_params)

    for table_data in tables_data:
        writer.save_records("muhtemeller", table_data)

    writer.close()

if __name__ == "__main__":
    main()
