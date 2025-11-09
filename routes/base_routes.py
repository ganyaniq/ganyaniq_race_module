from fastapi import APIRouter

router = APIRouter()

@router.get("/alfonso")
async def get_alfonso():
    return {
        "tahminler": [
            {"kosu": 1, "safkan": "ICE BOOM", "basari": 88},
            {"kosu": 2, "safkan": "WIND POWER", "basari": 79}
        ]
    }

@router.get("/surpriz")
async def get_surpriz():
    return {
        "sürprizler": [
            {"kosu": 3, "safkan": "GÖZDE KIZ", "oran": 14.5},
            {"kosu": 4, "safkan": "GECE KARTALI", "oran": 11.2}
        ]
    }
