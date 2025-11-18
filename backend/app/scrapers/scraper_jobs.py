from __future__ import annotations
import logging
from datetime import date, datetime, timedelta
import asyncio
from app.scrapers.tjk_advanced_scraper import tjk_advanced_scraper
from app.scrapers.ganyancanavari_scraper import ganyancanavari_scraper
from app.services.db_service import db_service

logger = logging.getLogger(__name__)

def run_daily_program_scraper():
    """Background job to scrape daily race program"""
    try:
        logger.info("[ScraperJob] Running daily program scraper...")
        
        # Scrape today's program
        today = date.today()
        races = tjk_scraper.scrape_daily_program(today)
        
        if races:
            # Save to database (using asyncio for async function)
            asyncio.run(db_service.save_race_program(today.isoformat(), races))
            logger.info(f"[ScraperJob] Saved {len(races)} races to database")
        else:
            logger.warning("[ScraperJob] No races found, using existing data")
    
    except Exception as e:
        logger.error(f"[ScraperJob] Error in daily program scraper: {e}")

def run_daily_results_scraper():
    """Background job to scrape daily race results"""
    try:
        logger.info("[ScraperJob] Running daily results scraper...")
        
        # Scrape today's results
        today = date.today()
        results = tjk_scraper.scrape_daily_results(today)
        
        if results:
            # Save to database
            asyncio.run(db_service.save_race_results(today.isoformat(), results))
            logger.info(f"[ScraperJob] Saved {len(results)} results to database")
        else:
            logger.info("[ScraperJob] No results found yet")
    
    except Exception as e:
        logger.error(f"[ScraperJob] Error in daily results scraper: {e}")

def run_program_update():
    """Update program periodically (before races start)"""
    try:
        logger.info("[ScraperJob] Checking for program updates...")
        run_daily_program_scraper()
    except Exception as e:
        logger.error(f"[ScraperJob] Error in program update: {e}")

def run_results_update():
    """Update results periodically (after races)"""
    try:
        logger.info("[ScraperJob] Checking for results updates...")
        run_daily_results_scraper()
    except Exception as e:
        logger.error(f"[ScraperJob] Error in results update: {e}")
