from fastapi import APIRouter
import csv

router = APIRouter()

@router.get("/sonuclar")
async def get_sonuclar():
    results = []
    with open("data/yaris_sonuclari.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            results.append(row)
    return results