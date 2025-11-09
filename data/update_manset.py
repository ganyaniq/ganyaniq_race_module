# update_manset.py
import json

def yeni_manset_ekle(dosya, manset):
    with open(dosya, encoding="utf-8") as f:
        data = json.load(f)
    data.insert(0, manset)
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Örnek çağırma:
yeni_manset_ekle("data/mansetler.json", {
    "tarih": "2025-06-01",
    "baslik": "Alfonso’dan İsabetli Tahmin",
    "icerik": "Alfonso 6’lı Ganyan'da 4 koşuyu doğru bildi.",
    "gorsel": "/static/images/alfonso_bildirdi.jpg"
})
