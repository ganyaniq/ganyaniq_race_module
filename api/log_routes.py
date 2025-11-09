from fastapi import APIRouter, Depends
from db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/logs", tags=["logs"])

@router.get("/")
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Burada gerçek logları veritabanından veya dosyadan okuyup döneceğiz
    # Şimdilik örnek dönüş
    return {"logs": "Log verisi henüz eklenmedi."}
