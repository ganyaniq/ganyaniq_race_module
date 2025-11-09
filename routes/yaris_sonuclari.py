import requests
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from db.database import get_db_session
from db.models import YarisSonuclari

router = APIRouter()

TJK_SONUCLAR_API = "https://www.tjk.org/TR/YarisSever/Sonuclar/GetSonuclar"

@router.get("/api/yaris-sonuclari")
async def get_yaris_sonuclari(db: Session = Depends(get_db_session)):
    try:
        response = requests.get(TJK_SONUCLAR_API)
        response.raise_for_status()
        sonuc_data = response.json()

        for item in sonuc_data.get("Sonuclar", []):
            if "Id" not in item or "Tarih" not in item or "Bilgiler" not in item:
                continue

            mevcut = db.query(YarisSonuclari).filter(YarisSonuclari.id == item["Id"]).first()

            if mevcut:
                mevcut.tarih = datetime.strptime(item["Tarih"], "%Y-%m-%dT%H:%M:%S")
                mevcut.bilgiler = item["Bilgiler"]
            else:
                yeni = YarisSonuclari(
                    id=item["Id"],
                    tarih=datetime.strptime(item["Tarih"], "%Y-%m-%dT%H:%M:%S"),
                    bilgiler=item["Bilgiler"]
                )
                db.add(yeni)

        db.commit()
        return JSONResponse(content={"status": "success", "message": "Yarış sonuçları güncellendi."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yarış sonuçları çekme hatası: {str(e)}")