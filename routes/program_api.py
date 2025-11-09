from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/api/yarisliste")
def get_yaris_programi():
    with open("data/yaris_programi.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
