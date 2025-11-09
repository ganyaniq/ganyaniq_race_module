from pydantic import BaseModel

class ReklamBannerCreate(BaseModel):
    title: str
    image_url: str
    link: str

    class Config:
        orm_mode = True

class ReklamBannerOut(ReklamBannerCreate):
    id: int
