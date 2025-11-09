from fastapi import APIRouter
import json
import os
from utils.updater import guncel_sayfalari_guncelle

router = APIRouter()

@router.get("/program/{tarih}")
def get_program(tarih: str):
    try:
        dosya_yolu = f"data/yaris_programi_{tarih}.json"
        if not os.path.exists(dosya_yolu):
            return {"hata": "Belirtilen tarihe ait program bulunamadı."}

        with open(dosya_yolu, "r", encoding="utf-8") as f:
            veri = json.load(f)

        # Program görüntülendiğinde en güncel sayfaları da güncelle
        guncel_sayfalari_guncelle()

        return {"tarih": tarih, "program": veri}

    except Exception as e:
        return {"hata": str(e)}
