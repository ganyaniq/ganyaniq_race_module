from fastapi import APIRouter

router = APIRouter()

@router.get("/{kategori_adi}")
async def get_kategori(kategori_adi: str):
    return {
        "kategori": kategori_adi,
        "haberler": [
            {"baslik": "Bugün Yarış Var", "link": "/haber/1"},
            {"baslik": "Favori Atlar Değişti", "link": "/haber/2"}
        ]
    }
