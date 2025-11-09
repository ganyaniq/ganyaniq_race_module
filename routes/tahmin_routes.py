from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from ai_training.tahmin_motoru import TahminMotoru
from db.database import get_db

router = APIRouter()
tahmin_motoru = TahminMotoru()

@router.get("/tahmin/{yarismaci_id}")
def tahmin_getir(yarismaci_id: int, db: Session = Depends(get_db)):
    try:
        sonuc = tahmin_motoru.tahmin_yap(yarismaci_id, db)
        return {"yarismaci_id": yarismaci_id, "tahmin": sonuc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
