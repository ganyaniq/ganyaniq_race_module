import requests
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from db.database import get_db_session
from db.models import YarisProgrami

router = APIRouter()

TJK_API_URL = "https://www.tjk.org/TR/YarisSever/Program/GetProgram"  # Gerçek URL ile değiştir

@router.get("/api/yaris-programi")
async def get_yaris_programi(db: Session = Depends(get_db_session)):
    try:
        response = requests.get(TJK_API_URL)
        response.raise_for_status()
        program_data = response.json()
        
        for item in program_data.get("Programlar", []):
            mevcut = db.query(YarisProgrami).filter(YarisProgrami.id == item["Id"]).first()
            if mevcut:
                mevcut.tarih = datetime.strptime(item["Tarih"], "%Y-%m-%dT%H:%M:%S")
                mevcut.bilgiler = item["Bilgiler"]
            else:
                yeni = YarisProgrami(
                    id=item["Id"],
                    tarih=datetime.strptime(item["Tarih"], "%Y-%m-%dT%H:%M:%S"),
                    bilgiler=item["Bilgiler"]
                )
                db.add(yeni)
        db.commit()
        return JSONResponse(content={"status": "success", "message": "Yarış programı güncellendi."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yarış programı çekme hatası: {str(e)}")
