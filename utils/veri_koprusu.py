
import csv
import os
from db.db_writer import DatabaseWriter

def islem_yap(csv_dosyasi):
    writer = DatabaseWriter()

    with open(csv_dosyasi, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = {
                "race_date": row.get("Tarih"),
                "track": row.get("Hipodrom"),
                "horse_name": row.get("At"),
                "jockey": row.get("Jokey"),
                "rank": int(row.get("Sıralama", 0)),
                "agf": float(row.get("AGF", 0.0)),
                "ganyan": float(row.get("Ganyan", 0.0)),
                "finish_time": row.get("Bitiş Süresi")
            }
            writer.write_race_result(data)

def klasor_icerigini_yukle(klasor_yolu):
    for dosya in os.listdir(klasor_yolu):
        if dosya.endswith(".csv"):
            tam_yol = os.path.join(klasor_yolu, dosya)
            print(f"İşleniyor: {tam_yol}")
            islem_yap(tam_yol)
