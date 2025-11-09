# routes/slider_routes.py

from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/api/haberler")
def haber_listele():
    try:
        with open("data/haberler.txt", "r", encoding="utf-8") as f:
            raw = f.read().split("---\n")
        haberler = []
        for h in raw:
            lines = h.strip().split("\n")
            if len(lines) >= 2:
                haberler.append({"baslik": lines[0], "icerik": lines[1]})
        return {"haberler": haberler}
    except:
        return {"haberler": []}

@router.get("/api/banners")
def banner_listele():
    try:
        with open("data/banners.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        banners = []
        for l in lines:
            parts = l.strip().split(",")
            if len(parts) == 3 and parts[2].lower() == "true":
                banners.append({"filename": parts[0], "link": parts[1]})
        return {"banners": banners}
    except:
        return {"banners": []}
