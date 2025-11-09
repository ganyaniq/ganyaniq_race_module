from fastapi import FastAPI
from api.kategori_routes import router as kategori_router
from api.log_routes import router as log_router

app = FastAPI(title="GANYANIQ API")

app.include_router(kategori_router)
app.include_router(log_router)

@app.get("/")
def root():
    return {"message": "GANYANIQ API çalışıyor."}
