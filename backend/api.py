from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Kategori(BaseModel):
    id: int
    name: str
    slug: str
    description: str

class AltKategoriItem(BaseModel):
    slug: str
    name: str
    description: str

class AltKategori(BaseModel):
    name: str
    items: List[AltKategoriItem]

class DetaySayfa(BaseModel):
    name: str
    description: str
    gecmis_kosular: List[str]
    agf: int
    son_sonuc: str

kategoriler = [
    {"id": 1, "name": "At Analizleri", "slug": "at-analizleri", "description": "Atlara dair güncel analizler."},
    {"id": 2, "name": "Jokey Performans", "slug": "jokey-performans", "description": "Jokeylerin yarış performansları."},
    {"id": 3, "name": "Yarış Programı", "slug": "yaris-programi", "description": "Güncel yarış programı detayları."},
]

alt_kategoriler_db = {
    "at-analizleri": {
        "name": "At Analizleri",
        "items": [
            {"slug": "safkan-1", "name": "Safkan 1", "description": "Detaylı analiz."},
            {"slug": "safkan-2", "name": "Safkan 2", "description": "Performans bilgileri."},
        ],
    },
    "jokey-performans": {
        "name": "Jokey Performans",
        "items": [
            {"slug": "jokey-1", "name": "Jokey 1", "description": "Yarış sonuçları."},
            {"slug": "jokey-2", "name": "Jokey 2", "description": "İstatistikler."},
        ],
    },
}

detay_db = {
    "safkan-1": {
        "name": "Safkan 1",
        "description": "Performans ve analiz detayları.",
        "gecmis_kosular": ["Koşu 1", "Koşu 2", "Koşu 3"],
        "agf": 85,
        "son_sonuc": "2. oldu",
    },
    "jokey-1": {
        "name": "Jokey 1",
        "description": "Jokey performans detayları.",
        "gecmis_kosular": ["Yarış 1", "Yarış 2"],
        "agf": 90,
        "son_sonuc": "1. oldu",
    },
}

@app.get("/api/kategoriler", response_model=List[Kategori])
async def get_kategoriler():
    return kategoriler

@app.get("/api/alt_kategori/{slug}", response_model=AltKategori)
async def get_alt_kategori(slug: str):
    if slug not in alt_kategoriler_db:
        raise HTTPException(status_code=404, detail="Alt kategori bulunamadı")
    return alt_kategoriler_db[slug]

@app.get("/api/detay/{slug}", response_model=DetaySayfa)
async def get_detay(slug: str):
    if slug not in detay_db:
        raise HTTPException(status_code=404, detail="Detay bulunamadı")
    return detay_db[slug]
