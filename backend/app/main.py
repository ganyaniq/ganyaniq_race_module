from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from contextlib import asynccontextmanager

from app.routers.api import router as api_router
from app.services.db_service import db_service
from app.config import ROOT_DIR
from app.libs.scheduler import Job, start_jobs
from app.scrapers.scraper_jobs import run_daily_program_scraper, run_daily_results_scraper

# Configure background jobs
SCRAPER_JOBS = [
    # Run program scraper every 2 hours (7200 seconds)
    Job("daily_program", 7200, run_daily_program_scraper),
    # Run results scraper every 5 minutes (300 seconds)
    Job("daily_results", 300, run_daily_results_scraper),
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup
    await db_service.connect()
    
    # DISABLED: Background scraper jobs (causing performance issues)
    # start_jobs(SCRAPER_JOBS)
    # print("[App] Started background scraper jobs")
    
    # DISABLED: Initial scrape (causing startup delay)
    # print("[App] Running initial data scrape...")
    # run_daily_program_scraper()
    
    print("[App] Ganyaniq Backend started successfully!")
    print("[App] Background jobs DISABLED for performance")
    
    yield
    
    # Shutdown
    await db_service.close()
    print("[App] Ganyaniq Backend shutdown complete")

app = FastAPI(title="Ganyaniq Backend", version="1.0.0", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="")

# Serve web UI
web_dir = ROOT_DIR.parent / "web"
if web_dir.exists():
    # Serve static files
    static_dir = web_dir / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    # Serve Ganyaniq UI at root
    @app.get("/")
    async def serve_ui():
        ui_path = web_dir / "ganyaniq.html"
        if ui_path.exists():
            return FileResponse(str(ui_path))
        return {"message": "Ganyaniq Backend - Web UI not found"}

@app.get("/health")
async def health_root():
    return {"ok": True, "status": "healthy"}

@app.get("/api/health")
async def health():
    return {"ok": True, "status": "healthy"}
