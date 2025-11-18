from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Horse(BaseModel):
    """Horse in a race"""
    name: str
    number: int
    jockey: Optional[str] = None
    trainer: Optional[str] = None
    owner: Optional[str] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    odds: Optional[float] = None

class Race(BaseModel):
    """Race model"""
    date: str  # YYYY-MM-DD
    hippodrome: str
    race_no: int
    race_name: Optional[str] = None
    distance: Optional[int] = None  # meters
    track_type: Optional[str] = None  # kum, çim, sentetik
    start_time: Optional[str] = None  # HH:MM
    horses: List[Horse] = Field(default_factory=list)
    status: str = "scheduled"  # scheduled, running, completed
    
class RaceResult(BaseModel):
    """Race result model"""
    date: str
    hippodrome: str
    race_no: int
    first: Optional[int] = None
    second: Optional[int] = None
    third: Optional[int] = None
    fourth: Optional[int] = None
    fifth: Optional[int] = None
    ganyan: Optional[float] = None
    plase: Optional[float] = None
    ikili: Optional[float] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
