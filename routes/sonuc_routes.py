from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.data_schemas import SonucVerisi
from db.models import Sonuc
from datetime import date

router = APIRouter()

@router.get("/sonuclar", response_model=list[SonucVerisi])
def sonuclari_getir(db: Session = Depends(get_db)):
    bugun = date.today()
    sonuclar = db.query(Sonuc).filter(Sonuc.tarih == bugun).all()
    return sonuclar
