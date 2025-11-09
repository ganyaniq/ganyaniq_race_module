# gecmis_tahmin.py
from database import get_db_session
from models import Tahmin
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/api/gecmis-tahminler")
async def get_gecmis_tahminler(db: Session = get_db_session()):
    try:
        tahminler = db.query(Tahmin).order_by(Tahmin.tarih.desc()).limit(100).all()
        sonuc = [
            {
                "yarismaci_id": t.yarismaci_id,
                "tahmin_degeri": t.tahmin_degeri,
                "tarih": t.tarih.isoformat()
            }
            for t in tahminler
        ]
        return JSONResponse(content=sonuc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geçmiş tahminler alınamadı: {str(e)}")
