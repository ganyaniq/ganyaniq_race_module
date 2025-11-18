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
    from app.services.data_service import data_service
    from datetime import datetime
    
    day_iso = _d2iso(day)
    target_date = datetime.fromisoformat(day_iso).date()
    
    # Try database first
    try:
        db_data = await db_service.get_race_program(day_iso)
        if db_data and "races" in db_data:
            return {"day": day_iso, "rows": db_data["races"], "source": "database"}
    except:
        pass
    
    # Refresh from live source
    try:
        races = await data_service.refresh_daily_program(target_date)
        if races:
            return {"day": day_iso, "rows": races, "source": "live"}
    except:
        pass
    
    # Fallback to sample
    sample_data = read_json("sample_program.json", [])
    rows = [r for r in sample_data if r.get("day") == day_iso]
    return {"day": day_iso, "rows": rows, "source": "sample"}

@router.get("/api/results-lite")
async def results_lite(day: str | None = None):
    """Get race results (lite version for UI)"""
    from app.services.data_service import data_service
    from datetime import datetime
    
    day_iso = _d2iso(day)
    target_date = datetime.fromisoformat(day_iso).date()
    
    # Try database
    try:
        db_data = await db_service.get_race_results(day_iso)
        if db_data and "results" in db_data:
            return {"day": day_iso, "rows": db_data["results"], "source": "database"}
    except:
        pass
    
    # Refresh from live
    try:
        results = await data_service.refresh_daily_results(target_date)
        if results:
            return {"day": day_iso, "rows": results, "source": "live"}
    except:
        pass
    
    # Fallback
    sample_data = read_json("sample_results.json", [])
    rows = [r for r in sample_data if r.get("day") == day_iso]
    return {"day": day_iso, "rows": rows, "source": "sample"}

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
    from app.services.additional_data_service import additional_data_service
    conditions = additional_data_service.get_weather_conditions()
    return {"ok": True, "stamp": datetime.now().isoformat(), "data": conditions}

@router.get("/api/weather")
async def api_weather():
    """Get weather (API route)"""
    from app.services.additional_data_service import additional_data_service
    conditions = additional_data_service.get_weather_conditions()
    return {"ok": True, "data": conditions}

@router.get("/api/news")
async def api_news():
    """Get news"""
    from app.services.additional_data_service import additional_data_service
    news = additional_data_service.get_news()
    return {"ok": True, "data": news}

@router.get("/api/stats")
async def api_stats():
    """Get statistics"""
    from app.services.additional_data_service import additional_data_service
    stats = additional_data_service.get_statistics()
    return {"ok": True, "data": stats}

@router.get("/api/probables-odds")
async def api_probables_odds(day: str | None = None):
    """Get probable odds"""
    from app.services.additional_data_service import additional_data_service
    from datetime import datetime
    day_iso = _d2iso(day)
    target_date = datetime.fromisoformat(day_iso).date()
    probables = additional_data_service.get_probables(target_date)
    return {"ok": True, "day": day_iso, "data": probables}

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

# Alfonso AI Predictions
@router.get("/api/predictions")
async def get_predictions(day: str | None = None):
    """Get Alfonso AI predictions for a day"""
    from app.ai.alfonso import alfonso_ai
    
    day_iso = _d2iso(day)
    
    # Get race program
    try:
        db_data = await db_service.get_race_program(day_iso)
        if not db_data or "races" not in db_data:
            return {"ok": True, "day": day_iso, "predictions": [], "message": "Yarış programı bulunamadı"}
        
        races = db_data["races"][:3]  # Only first 3 races to save credits
        predictions = []
        
        for race in races:
            try:
                pred = await alfonso_ai.analyze_race(race)
                predictions.append(pred)
            except Exception as e:
                print(f"[Alfonso] Error: {e}")
        
        return {"ok": True, "day": day_iso, "predictions": predictions, "count": len(predictions)}
    except Exception as e:
        print(f"[API] Prediction error: {e}")
        return {"ok": True, "day": day_iso, "predictions": [], "error": str(e)}

@router.post("/api/predictions/generate")
async def generate_predictions(day: str | None = None):
    """Force generate new predictions"""
    from app.services.prediction_service import prediction_service
    
    day_iso = _d2iso(day)
    predictions = await prediction_service.generate_daily_predictions(day_iso)
    
    return {"ok": True, "day": day_iso, "generated": len(predictions), "predictions": predictions}
