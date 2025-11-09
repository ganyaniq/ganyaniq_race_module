from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/admin/haberler", tags=["admin_haberler"])

# Haber model
class Haber(BaseModel):
    id: int
    title: str
    content: str
    image_url: Optional[str] = None
    is_manual: bool = False  # Manuel düzenleme işareti
    is_active: bool = True   # Görünürlük durumu

# Örnek veri deposu (DB yerine)
haber_db = []

@router.get("/", response_model=List[Haber])
async def listele():
    return [h for h in haber_db if h.is_active]

@router.get("/{haber_id}", response_model=Haber)
async def getir(haber_id: int):
    for h in haber_db:
        if h.id == haber_id:
            return h
    raise HTTPException(status_code=404, detail="Haber bulunamadı")

@router.put("/{haber_id}", response_model=Haber)
async def guncelle(haber_id: int, haber: Haber):
    for idx, h in enumerate(haber_db):
        if h.id == haber_id:
            haber_db[idx] = haber
            return haber
    raise HTTPException(status_code=404, detail="Haber bulunamadı")

@router.delete("/{haber_id}")
async def sil(haber_id: int):
    for h in haber_db:
        if h.id == haber_id:
            h.is_active = False
            return {"detail": "Haber pasif yapıldı"}
    raise HTTPException(status_code=404, detail="Haber bulunamadı")
