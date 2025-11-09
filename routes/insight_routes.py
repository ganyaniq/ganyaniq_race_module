from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/insight")
async def get_insight():
    with open("data/insight.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data