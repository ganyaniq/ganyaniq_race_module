from fastapi import APIRouter
import json
import os
from utils.updater import guncel_sayfalari_guncelle

router = APIRouter()

@router.get("/sonuc/{tarih}")
def get_sonuc(tarih: str):
    try:
        dosya_yolu = f"data/yaris_sonuclari_{tarih}.json"
        if not os.path.exists(dosya_yolu):
            return {"hata": "Belirtilen tarihe ait sonuç bulunamadı."}

        with open(dosya_yolu, "r", encoding="utf-8") as f:
            veri = json.load(f)

        # Sonuç görüntülendiğinde güncelleme tetiklenir
        guncel_sayfalari_guncelle()

        return {"tarih": tarih, "sonuclar": veri}

    except Exception as e:
        return {"hata": str(e)}
