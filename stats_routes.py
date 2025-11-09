from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/analizler", response_class=HTMLResponse)
async def analiz_panel(request: Request):
    return templates.TemplateResponse("analizler.html", {"request": request})
