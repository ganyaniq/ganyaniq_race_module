from fastapi import APIRouter, Query
from datetime import datetime
from typing import Optional, List, Dict, Any
from app.services.db_service import db_service
from app.libs.fs_cache import read_json

router = APIRouter()

def _d2iso(d: str | None) -> str:
    """Convert date to ISO format or use today"""
    if d:
        try:
            datetime.fromisoformat(d)
            return d
        except:
            pass
    return datetime.now().date().isoformat()

# ---- CORE (UI lite) ----
@router.get("/api/program-lite")
async def program_lite(day: str | None = None):
    """Get race program (lite version for UI)"""
    day_iso = _d2iso(day)
    
    # Try database first
    db_data = await db_service.get_race_program(day_iso)
    if db_data and "races" in db_data:
        return {"day": day_iso, "rows": db_data["races"]}
    
    # Fallback to sample data
    sample_data = read_json("sample_program.json", [])
    rows = [r for r in sample_data if r.get("day") == day_iso]
    return {"day": day_iso, "rows": rows}

@router.get("/api/results-lite")
async def results_lite(day: str | None = None):
    """Get race results (lite version for UI)"""
    day_iso = _d2iso(day)
    
    # Try database first
    db_data = await db_service.get_race_results(day_iso)
    if db_data and "results" in db_data:
        return {"day": day_iso, "rows": db_data["results"]}
    
    # Fallback to sample data
    sample_data = read_json("sample_results.json", [])
    rows = [r for r in sample_data if r.get("day") == day_iso]
    return {"day": day_iso, "rows": rows}

# ---- FULL API endpoints ----
@router.get("/program")
async def program(day: str | None = None):
    """Get full race program"""
    day_iso = _d2iso(day)
    db_data = await db_service.get_race_program(day_iso)
    return {"ok": True, "day": day_iso, "data": db_data or {}}

@router.get("/results")
async def results(day: str | None = None):
    """Get full race results"""
    day_iso = _d2iso(day)
    db_data = await db_service.get_race_results(day_iso)
    return {"ok": True, "day": day_iso, "data": db_data or {}}

@router.get("/news")
async def get_news(limit: int = 10):
    """Get latest news"""
    news = await db_service.get_latest_news(limit)
    return {"ok": True, "data": news}

@router.get("/probables")
async def probables(day: str | None = None):
    """Get probable odds"""
    return {"ok": True, "day": _d2iso(day), "data": []}

@router.get("/weather")
async def weather():
    """Get weather and track conditions"""
    return {"ok": True, "stamp": datetime.now().isoformat(), "data": []}

@router.get("/entities/horse")
async def entity_horse(name: str):
    """Get horse details"""
    return {"ok": True, "name": name, "data": {}}

@router.get("/entities/jockey")
async def entity_jockey(name: str):
    """Get jockey details"""
    return {"ok": True, "name": name, "data": {}}

@router.get("/api/health")
async def api_health():
    """Health check endpoint"""
    return {"ok": True, "status": "healthy", "timestamp": datetime.now().isoformat()}
