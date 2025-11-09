from fastapi import APIRouter

router = APIRouter()

@router.get("/program")
async def get_program():
    return {
        "program": [
            {"kosu": 1, "saat": "14:00", "safkanlar": ["ICE BOOM", "THUNDER ROAD"]},
            {"kosu": 2, "saat": "14:30", "safkanlar": ["WIND POWER", "GÖK ATLISI"]}
        ]
    }

@router.get("/sonuclar")
async def get_sonuclar():
    return {
        "sonuclar": [
            {"kosu": 1, "kazanan": "ICE BOOM", "ikincilik": "THUNDER ROAD"},
            {"kosu": 2, "kazanan": "WIND POWER", "ikincilik": "GÖK ATLISI"}
        ]
    }
