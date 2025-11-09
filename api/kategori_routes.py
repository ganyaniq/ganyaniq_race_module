from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db import crud
from models import KategoriVeri
from pydantic import BaseModel

router = APIRouter(prefix="/kategori", tags=["kategori"])

class KategoriCreate(BaseModel):
    title: str
    description: str = None

@router.get("/")
def read_kategoriler(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    kategoriler = crud.get_kategori_veri(db, skip=skip, limit=limit)
    return kategoriler

@router.get("/{kategori_id}")
def read_kategori(kategori_id: int, db: Session = Depends(get_db)):
    kategori = crud.get_kategori_veri_by_id(db, kategori_id)
    if not kategori:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    return kategori

@router.post("/")
def create_kategori(kategori: KategoriCreate, db: Session = Depends(get_db)):
    created = crud.create_kategori_veri(db, title=kategori.title, description=kategori.description)
    return created

@router.delete("/{kategori_id}")
def delete_kategori(kategori_id: int, db: Session = Depends(get_db)):
    success = crud.delete_kategori_veri(db, kategori_id)
    if not success:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    return {"detail": "Kategori silindi"}
