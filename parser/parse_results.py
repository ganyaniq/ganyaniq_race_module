# parser/parse_results.py
import csv

def parse_results(csv_path):
    results = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            results.append({
                "tarih": row.get("Tarih"),
                "kosu_no": row.get("KoşuNo"),
                "kosu_adi": row.get("KoşuAdı"),
                "at_ismi": row.get("At"),
                "jokey": row.get("Jokey"),
                "antrenor": row.get("Antrenör"),
                "ganyan": row.get("Ganyan"),
                "derece": row.get("Derece"),
                "sira": row.get("Sıra"),
                "mesafe": row.get("Mesafe"),
                "pist": row.get("Pist")
            })
    return results
