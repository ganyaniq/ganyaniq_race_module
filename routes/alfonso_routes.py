from fastapi import APIRouter, UploadFile, File
from predictor import predict_from_csv
from train_alfonso import train_model

router = APIRouter()

@router.post("/train-alfonso")
async def train_alfonso_endpoint():
    result = train_model()
    return {"message": result}

@router.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(contents)

        predictions = predict_from_csv(file_path)
        return {"tahminler": predictions}

    except Exception as e:
        return {"error": str(e)}
