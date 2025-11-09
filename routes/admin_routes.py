from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import PlainTextResponse
import shutil, os

router = APIRouter()

# CSV Yükleme
@router.post("/admin/upload-csv")
async def upload_csv(csv_file: UploadFile = File(...)):
    path = f"data/uploads/{csv_file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(csv_file.file, buffer)
    return {"message": f"CSV yüklendi: {csv_file.filename}"}

# Alfonso Eğitimi Başlat
@router.post("/admin/train-alfonso")
async def train_alfonso():
    os.system("python alfonso/train_alfonso.py")
    return {"message": "Alfonso eğitimi başlatıldı"}

# Logları Görüntüle
@router.get("/admin/logs", response_class=PlainTextResponse)
async def get_logs():
    try:
        with open("log_raporu.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Log dosyası bulunamadı."

# Haber Ekleme
@router.post("/admin/haber-ekle")
async def haber_ekle(title: str = Form(...), content: str = Form(...)):
    with open("data/haberler.txt", "a", encoding="utf-8") as f:
        f.write(f"{title}\n{content}\n---\n")
    return {"message": "Haber eklendi."}

# Banner Yükleme
@router.post("/admin/banner-ekle")
async def banner_ekle(banner: UploadFile = File(...), link: str = Form(...), active: bool = Form(...)):
    save_path = f"static/banners/{banner.filename}"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(banner.file, buffer)

    with open("data/banners.txt", "a", encoding="utf-8") as f:
        f.write(f"{banner.filename},{link},{active}\n")

    return {"message": "Banner başarıyla kaydedildi."}
