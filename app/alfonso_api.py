# alfonso_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Tahmin(BaseModel):
    kosu_id: int
    at_id: int
    olasilik: float
    icgoru_notu: str

fake_tahminler = [
    {"kosu_id": 101, "at_id": 201, "olasilik": 0.35, "icgoru_notu": "Pist çok ağır, performans etkilenebilir."},
    {"kosu_id": 101, "at_id": 202, "olasilik": 0.25, "icgoru_notu": "Son idmanlar iyi, yükselişte."},
]

@app.get("/tahminler/{kosu_id}", response_model=List[Tahmin])
async def get_tahminler(kosu_id: int):
    return [t for t in fake_tahminler if t['kosu_id'] == kosu_id]
