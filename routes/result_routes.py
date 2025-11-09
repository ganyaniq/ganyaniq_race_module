from fastapi import APIRouter
import csv

router = APIRouter()

@router.get("/result/{race_id}")
async def get_result_by_id(race_id: str):
    with open("data/yaris_sonuclari.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["race_id"] == race_id:
                return row
    return {"error": "Race not found"}