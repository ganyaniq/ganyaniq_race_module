from fastapi import APIRouter
import json
import os

router = APIRouter()

@router.get("/detay/{kosu_id}")
def get_kosu_detay(kosu_id: str):
    try:
        # Detay dosyası varsayılan olarak templates/kosu içinde yer alır
        dosya_yolu = f"templates/kosu/{kosu_id}.html"
        if not os.path.exists(dosya_yolu):
            return {"hata": "Belirtilen koşu ID'sine ait detay sayfası bulunamadı."}

        with open(dosya_yolu, "r", encoding="utf-8") as f:
            icerik = f.read()

        return {"kosu_id": kosu_id, "html": icerik}

    except Exception as e:
        return {"hata": str(e)}
