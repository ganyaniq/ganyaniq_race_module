from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import shutil
import os
from subprocess import Popen

router = APIRouter()

DATA_DIR = "data"
LOG_FILE = "log_raporu.txt"
ALFONSO_TRAIN_SCRIPT = "train_alfonso.py"

os.makedirs(DATA_DIR, exist_ok=True)

@router.post("/admin/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    file_location = os.path.join(DATA_DIR, file.filename)
    try:
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})

@router.get("/admin/logs")
def get_logs():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "success", "log": content}
    except FileNotFoundError:
        return {"status": "error", "log": "Log dosyası bulunamadı."}

@router.post("/admin/train-alfonso")
def trigger_alfonso_training():
    try:
        if not os.path.exists(ALFONSO_TRAIN_SCRIPT):
            return {"status": "error", "detail": "Eğitim scripti bulunamadı."}
        # Alfonso eğitim scriptini başlat
        Popen(["python", ALFONSO_TRAIN_SCRIPT])
        return {"status": "started", "detail": "Alfonso eğitimi başlatıldı."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
