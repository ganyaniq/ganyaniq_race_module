from fastapi import APIRouter
from typing import List
from models import Haber, HaberDetay
from db_writer import fetch_haberler, fetch_haber_detay

router = APIRouter()

@router.get("/haberler", response_model=List[Haber])
async def get_haberler():
    return await fetch_haberler()

@router.get("/haberler/{haber_id}", response_model=HaberDetay)
async def get_haber_detay(haber_id: int):
    return await fetch_haber_detay(haber_id)
