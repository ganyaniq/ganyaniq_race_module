
import os
import json
from datetime import datetime

def en_guncel_tahmin_dosyasi(logs_klasoru="logs"):
    dosyalar = [f for f in os.listdir(logs_klasoru) if f.endswith(".json")]
    if not dosyalar:
        return None
    dosyalar.sort(reverse=True)
    return os.path.join(logs_klasoru, dosyalar[0])

def grafik_verisi_hazirla():
    dosya = en_guncel_tahmin_dosyasi()
    if not dosya:
        return {}

    with open(dosya, "r", encoding="utf-8") as f:
        veri = json.load(f)

    tahminler = veri.get("data", [])

    favori_sayisi = 0
    surpriz_sayisi = 0
    toplam_kosu = len(tahminler)

    favori_siralar = []
    for t in tahminler:
        if t.get("tahmin"):
            sira = t["tahmin"][0].get("sira", 0)
            favori_siralar.append(sira)
            if sira == 1:
                favori_sayisi += 1
            elif sira >= 4:
                surpriz_sayisi += 1

    ortalama_sira = round(sum(favori_siralar)/len(favori_siralar), 2) if favori_siralar else 0

    return {
        "toplam_kosu": toplam_kosu,
        "favori": favori_sayisi,
        "surpriz": surpriz_sayisi,
        "ortalama_sira": ortalama_sira
    }
