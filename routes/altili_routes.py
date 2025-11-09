
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import json
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def son_tahmin_json():
    logs_klasoru = "logs"
    dosyalar = [f for f in os.listdir(logs_klasoru) if f.endswith(".json")]
    if not dosyalar:
        return []

    dosyalar.sort(reverse=True)
    en_son = os.path.join(logs_klasoru, dosyalar[0])

    with open(en_son, "r", encoding="utf-8") as f:
        veri = json.load(f)

    return veri.get("data", [])

@router.get("/altili")
async def altili_sayfasi(request: Request):
    tahminler = son_tahmin_json()
    return templates.TemplateResponse("altili.html", {
        "request": request,
        "tahminler": tahminler
    })
