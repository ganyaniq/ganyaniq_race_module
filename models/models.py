from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Kategori(Base):
    __tablename__ = 'kategoriler'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    alt_kategoriler = relationship('AltKategori', back_populates='kategori')

class AltKategori(Base):
    __tablename__ = 'alt_kategoriler'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    kategori_id = Column(Integer, ForeignKey('kategoriler.id'))

    kategori = relationship('Kategori', back_populates='alt_kategoriler')
    detaylar = relationship('Detay', back_populates='alt_kategori')

class Detay(Base):
    __tablename__ = 'detaylar'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    slug = Column(String, unique=True, index=True)
    content = Column(Text)
    published_at = Column(DateTime, default=datetime.utcnow)
    alt_kategori_id = Column(Integer, ForeignKey('alt_kategoriler.id'))

    alt_kategori = relationship('AltKategori', back_populates='detaylar')

class Haber(Base):
    __tablename__ = 'haberler'

    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String, index=True)
    ozet = Column(Text)
    icerik = Column(Text)
    yayin_tarihi = Column(DateTime, default=datetime.utcnow)
    resim_url = Column(String, nullable=True)
    video_link = Column(String, nullable=True)
