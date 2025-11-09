
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from tahmin_utils import altili_tahmin_al, icgoru_notu_uret

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/kupon")
async def kupon_sayfasi(request: Request):
    tahminler = altili_tahmin_al()
    icgoruler = []

    for kosu in tahminler:
        icgoru = icgoru_notu_uret(kosu)
        icgoruler.append(icgoru)

    return templates.TemplateResponse("kupon.html", {
        "request": request,
        "tahminler": tahminler,
        "icgoruler": icgoruler
    })
