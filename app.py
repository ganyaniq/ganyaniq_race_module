from routes import tahmin_routes
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.models import create_tables
from routes import admin_routes, kategori_routes, ai_trigger

app = FastAPI()

create_tables()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(admin_routes.router, prefix="/admin")
app.include_router(kategori_routes.router, prefix="/kategori")
app.include_router(ai_trigger.router, prefix="/ai-trigger")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=10000, reload=True)


app.include_router(tahmin_routes.router)

app.include_router(tahmin_routes.router, prefix="/tahmin")
