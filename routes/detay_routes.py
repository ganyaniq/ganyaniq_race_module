# ganyaniq_race_module/routes/detay_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Yarismaci
from schemas.data_schemas import YarismaciGiris

router = APIRouter()

@router.get("/detay/{kosu_id}", response_model=list[YarismaciGiris])
def detay_getir(kosu_id: int, db: Session = Depends(get_db)):
    yarismacilar = db.query(Yarismaci).filter(Yarismaci.kosu_id == kosu_id).all()
    if not yarismacilar:
        raise HTTPException(status_code=404, detail="Koşu bulunamadı")
    return yarismacilar
