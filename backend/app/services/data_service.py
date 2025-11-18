import logging
from datetime import date
from app.scrapers.tjk_live_scraper import tjk_live
from app.services.db_service import db_service

logger = logging.getLogger(__name__)

class DataService:
    async def refresh_daily_program(self, target_date=None):
        if not target_date:
            target_date = date.today()
        
        races = tjk_live.get_daily_program(target_date)
        
        if races:
            await db_service.save_race_program(target_date.isoformat(), races)
            logger.info(f"Refreshed program: {len(races)} races")
            return races
        return []
    
    async def refresh_daily_results(self, target_date=None):
        if not target_date:
            target_date = date.today()
        
        results = tjk_live.get_daily_results(target_date)
        
        if results:
            await db_service.save_race_results(target_date.isoformat(), results)
            logger.info(f"Refreshed results: {len(results)} results")
            return results
        return []

data_service = DataService()
