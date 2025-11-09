from fastapi import APIRouter

router = APIRouter()

@router.post("/trigger")
async def ai_trigger():
    # Burada AI tahmin fonksiyonunu tetikle
    print("AI tetikleyici çalıştı")  # Log için
    return {"mesaj": "AI tetikleyici çalıştı ve işlem tamamlandı"}
