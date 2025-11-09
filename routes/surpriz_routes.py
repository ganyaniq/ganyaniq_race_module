
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def getir_surpriz_tahminler():
    logs_klasoru = "logs"
    dosyalar = [f for f in os.listdir(logs_klasoru) if f.endswith(".json")]
    if not dosyalar:
        return []

    dosyalar.sort(reverse=True)
    son_dosya = os.path.join(logs_klasoru, dosyalar[0])

    with open(son_dosya, "r", encoding="utf-8") as f:
        veri = json.load(f)

    tahminler = veri.get("data", [])
    surpriz_listesi = []

    for index, kosu in enumerate(tahminler, start=1):
        surprizler = [at for at in kosu.get("tahmin", []) if at.get("sira", 0) >= 4]
        if surprizler:
            surpriz_listesi.append({
                "kosu_no": index,
                "surprizler": surprizler
            })

    return surpriz_listesi

@router.get("/surprizatlar")
async def surpriz_sayfasi(request: Request):
    veri = getir_surpriz_tahminler()
    return templates.TemplateResponse("surprizatlar.html", {
        "request": request,
        "kosular": veri
    })
