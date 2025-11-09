
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/analizler", response_class=HTMLResponse)
async def analiz_sayfasi(request: Request):
    return templates.TemplateResponse("analizler.html", {"request": request})
