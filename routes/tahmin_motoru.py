from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import Yarismaci, Tahmin
from database import get_db
from schemas.data_schemas import TahminOut
from typing import List
from tahmin_motoru import alfonso_tahmin_yap
from datetime import datetime

router = APIRouter()

@router.post("/predict/{kosu_id}", response_model=List[TahminOut])
def tahmin_al(kosu_id: int, db: Session = Depends(get_db)):
    # Kosuya ait yarışmacıları al
    yarismacilar = db.query(Yarismaci).filter(Yarismaci.kosu_id == kosu_id).all()

    # AI tahmin motorunu çağır
    tahmin_sonuclari = alfonso_tahmin_yap(yarismacilar)

    # Sonuçları veritabanına kaydet ve geri döndür
    tahmin_kaydi = []
    for sonuc in tahmin_sonuclari:
        kayit = Tahmin(
            yarismaci_id=sonuc["yarismaci_id"],
            tahmin=sonuc["tahmin"],
            kazanma_ihtimali=sonuc["kazanma_ihtimali"],
            icerik_notu=sonuc.get("icerik_notu", None),
            tahmin_tarihi=datetime.utcnow()
        )
        db.add(kayit)
        tahmin_kaydi.append(kayit)
    db.commit()

    return tahmin_kaydi
