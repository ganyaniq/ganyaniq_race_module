import logging
from datetime import date
from app.scrapers.tjk_real_scraper import tjk_real_scraper
from app.scrapers.tjk_live_scraper import tjk_live
from app.services.db_service import db_service

logger = logging.getLogger(__name__)

class DataService:
    async def refresh_daily_program(self, target_date=None):
        if not target_date:
            target_date = date.today()
        
        # Try real TJK first
        races = tjk_real_scraper.get_daily_program(target_date)
        
        # Fallback to generated data if real scraping fails
        if not races or len(races) == 0:
            logger.info("[DataService] Real scraping failed, using fallback")
            races = tjk_live.get_daily_program(target_date)
        
        if races:
            await db_service.save_race_program(target_date.isoformat(), races)
            logger.info(f"[DataService] Saved {len(races)} races")
            return races
        return []
    
    async def refresh_daily_results(self, target_date=None):
        if not target_date:
            target_date = date.today()
        
        # Try real TJK first
        results = tjk_real_scraper.get_daily_results(target_date)
        
        # Fallback to generated data
        if not results or len(results) == 0:
            logger.info("[DataService] Real results failed, using fallback")
            results = tjk_live.get_daily_results(target_date)
        
        if results:
            await db_service.save_race_results(target_date.isoformat(), results)
            logger.info(f"[DataService] Saved {len(results)} results")
            return results
        return []

data_service = DataService()
