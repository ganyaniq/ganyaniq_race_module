from pydantic import BaseModel, Field
from typing import Optional

class AlfonsoVerisi(BaseModel):
    yas: int = Field(..., ge=1, le=15)
    jokey_puani: int = Field(..., ge=0, le=100)
    son_3_yaris: str
    agf: float = Field(..., ge=0.0)
    galop_puani: float = Field(..., ge=0.0)
    kazandi: Optional[int] = Field(None, ge=0, le=1)
