import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "ganyaniq_race_module"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.alfonso_routes import router as alfonso_router

app = FastAPI(title="GANYAN IQ API", description="Alfonso Tahmin Sistemi", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alfonso_router)

@app.get("/")
def root():
    return {"mesaj": "GANYAN IQ API’ye hoş geldin! Bu API Alfonso tahmin sistemiyle çalışır."}
