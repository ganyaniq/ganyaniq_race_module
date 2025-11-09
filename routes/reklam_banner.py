from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db_session
from db.models import ReklamBanner
from db.schemas import ReklamBannerCreate, ReklamBannerOut

router = APIRouter()

@router.post("/reklam", response_model=ReklamBannerOut)
def create_reklam_banner(banner: ReklamBannerCreate, db: Session = Depends(get_db_session)):
    db_banner = ReklamBanner(**banner.dict())
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return db_banner
