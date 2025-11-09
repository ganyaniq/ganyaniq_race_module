# main.py
from fastapi import FastAPI
from yaris_programi_scraper import fetch_daily_program, write_to_db
from yaris_sonuclari_scraper import fetch_race_results, write_results_to_db
from alfonso_api import app as alfonso_app

app = FastAPI()

app.mount("/alfonso", alfonso_app)

@app.get("/program/guncelle")
async def update_program():
    program = fetch_daily_program()
    write_to_db(program)
    return {"status": "Yarış programı güncellendi."}

@app.get("/sonuclar/guncelle")
async def update_results():
    from datetime import datetime
    results = fetch_race_results(datetime.today())
    write_results_to_db(results)
    return {"status": "Yarış sonuçları güncellendi."}
