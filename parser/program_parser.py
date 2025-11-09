import csv
import json
from datetime import datetime

def parse_yaris_programi(csv_path="veri/yaris_programi.csv", json_path="data/yaris_programi.json"):
    data = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                "kosu_no": int(row["KosuNo"]),
                "saat": row["Saat"],
                "mesafe": int(row["Mesafe"]),
                "pist": row["Pist"],
                "at_sayisi": int(row["AtSayisi"]),
                "hipodrom": row["Hipodrom"],
                "yaris_gunu": row.get("Tarih") or datetime.today().strftime('%Y-%m-%d')
            })

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return data
