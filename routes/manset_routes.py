
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/mansetler")
async def manset_sayfasi(request: Request):
    manset_liste = [
        {"baslik": "Favori Atların Gücü Bugün Test Ediliyor", "tarih": datetime.today().strftime("%d.%m.%Y"), "etiket": "Favori", "kaynak": "Alfonso AI"},
        {"baslik": "Sürpriz Koşularda Alfonso'dan Uyarılar Var", "tarih": datetime.today().strftime("%d.%m.%Y"), "etiket": "Sürpriz", "kaynak": "Alfonso AI"},
        {"baslik": "Günün Kritik 4. Koşusunda Pist Değişikliği", "tarih": datetime.today().strftime("%d.%m.%Y"), "etiket": "Pist", "kaynak": "Hipodrom Veri"},
    ]
    return templates.TemplateResponse("mansetler.html", {
        "request": request,
        "mansetler": manset_liste
    })
