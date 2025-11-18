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
    from app.libs.cache import cache
    from datetime import datetime
    
    day_iso = _d2iso(day)
    
    # Check cache first (5 min)
    cache_key = f"program_{day_iso}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    target_date = datetime.fromisoformat(day_iso).date()
    
    # Try database
    try:
        db_data = await db_service.get_race_program(day_iso)
        if db_data and "races" in db_data:
            result = {"day": day_iso, "rows": db_data["races"], "source": "database"}
            cache.set(cache_key, result)
            return result
    except:
        pass
    
    # Refresh from live
    try:
        races = await data_service.refresh_daily_program(target_date)
        if races:
            result = {"day": day_iso, "rows": races, "source": "live"}
            cache.set(cache_key, result)
            return result
    except:
        pass
    
    # Fallback
    sample_data = read_json("sample_program.json", [])
    rows = [r for r in sample_data if r.get("day") == day_iso]
    result = {"day": day_iso, "rows": rows, "source": "sample"}
    cache.set(cache_key, result, 60)
    return result

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

@router.post("/api/refresh-data")
async def refresh_data(day: str | None = None):
    """Force refresh data from TJK"""
    from app.services.data_service import data_service
    from datetime import datetime
    
    day_iso = _d2iso(day)
    target_date = datetime.fromisoformat(day_iso).date()
    
    # Refresh program and results
    program = await data_service.refresh_daily_program(target_date)
    results = await data_service.refresh_daily_results(target_date)
    
    return {
        "ok": True,
        "day": day_iso,
        "program_count": len(program),
        "results_count": len(results),
        "message": "Data refreshed from TJK"
    }

@router.get("/api/mick-surprises")
async def mick_surprises(day: str | None = None):
    """Mick AI - Sürpriz atlar"""
    from app.ai.mick import mick_ai
    day_iso = _d2iso(day)
    
    try:
        db_data = await db_service.get_race_program(day_iso)
        if db_data and "races" in db_data:
            surprises = await mick_ai.find_surprise_horses(db_data["races"])
            return {"ok": True, "day": day_iso, "surprises": surprises}
    except:
        pass
    
    return {"ok": True, "day": day_iso, "surprises": []}

@router.get("/api/arion-insights")
async def arion_insights(day: str | None = None):
    """Arion AI - İçgörüler"""
    from app.ai.arion import arion_ai
    day_iso = _d2iso(day)
    
    try:
        db_data = await db_service.get_race_program(day_iso)
        if db_data and "races" in db_data:
            insights = await arion_ai.generate_insights(db_data["races"])
            return {"ok": True, "day": day_iso, "insights": insights}
    except:
        pass
    
    return {"ok": True, "day": day_iso, "insights": []}

@router.get("/api/hermes-notifications")
async def hermes_notifications():
    """Hermes AI - Bildirimler"""
    from app.ai.hermes import hermes_ai
    
    try:
        notifications = await hermes_ai.generate_notifications()
        return {"ok": True, "notifications": notifications}
    except:
        pass
    
    return {"ok": True, "notifications": []}

@router.get("/api/lyra-charts")
async def lyra_charts(day: str | None = None):
    """Lyra AI - Grafik verileri"""
    from app.ai.lyra import lyra_ai
    day_iso = _d2iso(day)
    
    try:
        db_data = await db_service.get_race_program(day_iso)
        if db_data and "races" in db_data:
            charts = await lyra_ai.generate_chart_data(db_data["races"])
            return {"ok": True, "day": day_iso, "charts": charts}
    except:
        pass
    
    return {"ok": True, "day": day_iso, "charts": []}

@router.get("/api/lyra-trends")
async def lyra_trends(horse_id: str | None = None):
    """Lyra AI - Performans trendleri"""
    from app.ai.lyra import lyra_ai
    
    try:
        trend = await lyra_ai.get_performance_trends(horse_id)
        return {"ok": True, "trend": trend}
    except:
        pass
    
    return {"ok": True, "trend": {}}

@router.get("/api/gc-declarations")
async def gc_declarations():
    """Ganyancanavari - Deklareler"""
    from app.scrapers.ganyancanavari_scraper import ganyancanavari_scraper
    
    declarations = ganyancanavari_scraper.get_declarations()
    return {"ok": True, "data": declarations}

@router.get("/api/gc-workouts")
async def gc_workouts():
    """Ganyancanavari - Galoplar"""
    from app.scrapers.ganyancanavari_scraper import ganyancanavari_scraper
    
    workouts = ganyancanavari_scraper.get_workouts()
    return {"ok": True, "data": workouts}

@router.get("/api/admin/stats")
async def admin_stats():
    """Admin - Sistem istatistikleri"""
    from app.services.admin_service import admin_service
    
    stats = await admin_service.get_system_stats()
    return {"ok": True, "stats": stats}

@router.post("/api/admin/clear-cache")
async def admin_clear_cache():
    """Admin - Cache temizle"""
    from app.services.admin_service import admin_service
    
    result = await admin_service.clear_cache()
    return result

@router.get("/api/admin/logs")
async def admin_logs(limit: int = 50):
    """Admin - Log kayıtları"""
    from app.services.admin_service import admin_service
    
    logs = await admin_service.get_recent_logs(limit)
    return {"ok": True, "logs": logs}

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
