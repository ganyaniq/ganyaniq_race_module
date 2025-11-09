from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.data_schemas import ProgramVerisi
from db.models import Program
from datetime import date

router = APIRouter()

@router.get("/program", response_model=list[ProgramVerisi])
def programlari_getir(db: Session = Depends(get_db)):
    bugun = date.today()
    programlar = db.query(Program).filter(Program.tarih == bugun).all()
    return programlar
