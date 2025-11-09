# affiliate_api.py
import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

AFFILIATE_API_BASE = "https://affiliateapi.example.com"
API_KEY = "YOUR_API_KEY"  # .env dosyasından çekilmeli, burada örnek olarak yazıldı

@router.get("/api/affiliate-links")
async def get_affiliate_links():
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(f"{AFFILIATE_API_BASE}/links", headers=headers)
        response.raise_for_status()
        links = response.json()
        return JSONResponse(content=links)
    except requests.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Affiliate API hatası: {str(e)}")
