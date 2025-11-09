from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.models import Kategori
from db.db_writer import DBWriter
from db.database import get_db
from pydantic import BaseModel

router = APIRouter()

class KategoriIn(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None

@router.post("/kategoriler/batch")
def add_update_kategoriler(kategoriler: List[KategoriIn], db: Session = Depends(get_db)):
    writer = DBWriter(db)
    kategoriler_dict = [kat.dict() for kat in kategoriler]
    writer.upsert_kategoriler(kategoriler_dict)
    return {"status": "başarılı", "message": f"{len(kategoriler)} kategori işlendi."}

@router.get("/kategoriler", response_model=List[Kategori])
def get_kategoriler(db: Session = Depends(get_db)):
    kategoriler = db.query(Kategori).all()
    if not kategoriler:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    return kategoriler
