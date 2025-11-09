# parser/parse_program.py
import json

def parse_program(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    parsed = []
    for race in data.get("yarislar", []):
        parsed.append({
            "tarih": race.get("tarih"),
            "saat": race.get("saat"),
            "kosu_no": race.get("kosu_no"),
            "kosu_adi": race.get("kosu_adi"),
            "hipodrom": race.get("hipodrom"),
            "mesafe": race.get("mesafe"),
            "pist": race.get("pist"),
            "hava": race.get("hava"),
            "atlar": race.get("atlar", [])  # Atlar artık detaylı JSON
        })
    return parsed
