from sqlalchemy.orm import Session
from models import KategoriVeri

def get_kategori_veri(db: Session, skip: int = 0, limit: int = 100):
    return db.query(KategoriVeri).offset(skip).limit(limit).all()

def get_kategori_veri_by_id(db: Session, kategori_id: int):
    return db.query(KategoriVeri).filter(KategoriVeri.id == kategori_id).first()

def create_kategori_veri(db: Session, title: str, description: str = None):
    db_item = KategoriVeri(title=title, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_kategori_veri(db: Session, kategori_id: int):
    obj = db.query(KategoriVeri).filter(KategoriVeri.id == kategori_id).first()
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
