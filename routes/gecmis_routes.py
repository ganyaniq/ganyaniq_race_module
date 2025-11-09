
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os
import json
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def son_uc_tahmin():
    logs_klasoru = "logs"
    dosyalar = [f for f in os.listdir(logs_klasoru) if f.endswith(".json")]
    dosyalar.sort(reverse=True)
    secilenler = dosyalar[:3]

    tum_tahminler = []

    for dosya in secilenler:
        dosya_yolu = os.path.join(logs_klasoru, dosya)
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            icerik = json.load(f)
            tarih = dosya.replace("altili_", "").replace(".json", "")
            tarih_okunabilir = datetime.strptime(tarih, "%Y%m%d_%H%M").strftime("%d.%m.%Y %H:%M")
            tum_tahminler.append({
                "tarih": tarih_okunabilir,
                "kosular": icerik.get("data", [])
            })

    return tum_tahminler

@router.get("/gecmistahmin")
async def gecmis_tahmin_sayfasi(request: Request):
    veri = son_uc_tahmin()
    return templates.TemplateResponse("gecmistahmin.html", {
        "request": request,
        "gecmisler": veri
    })
