from __future__ import annotations
import re
import logging
from datetime import date
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from app.libs.net_client import get

logger = logging.getLogger(__name__)

GC_BASE = "https://www.ganyancanavari.com"

class GanyancanavarScraper:
    """Ganyancanavari.com scraper"""
    
    def scrape_declarations(self) -> List[Dict[str, Any]]:
        """
        Scrape declarations (deklareler)
        """
        try:
            url = f"{GC_BASE}/site/deklareler.html"
            logger.info("[GC Scraper] Scraping declarations...")
            
            response = get(url, referer=GC_BASE)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            declarations = []
            
            # Parse declarations table
            tables = soup.find_all('table')
            for table in tables[:5]:
                rows = table.find_all('tr')[1:]
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        decl = {
                            "horse": cols[0].get_text(strip=True),
                            "status": cols[1].get_text(strip=True),
                            "date": date.today().isoformat()
                        }
                        declarations.append(decl)
            
            logger.info(f"[GC Scraper] Scraped {len(declarations)} declarations")
            return declarations
            
        except Exception as e:
            logger.error(f"[GC Scraper] Error scraping declarations: {e}")
            return []
    
    def scrape_entries(self) -> List[Dict[str, Any]]:
        """
        Scrape entries (kayıtlar)
        """
        try:
            url = f"{GC_BASE}/site/kayitlar.html"
            logger.info("[GC Scraper] Scraping entries...")
            
            response = get(url, referer=GC_BASE)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            entries = []
            
            # Parse entries
            tables = soup.find_all('table')
            for table in tables[:5]:
                rows = table.find_all('tr')[1:]
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        entry = {
                            "horse": cols[0].get_text(strip=True),
                            "race_info": cols[1].get_text(strip=True),
                            "date": date.today().isoformat()
                        }
                        entries.append(entry)
            
            logger.info(f"[GC Scraper] Scraped {len(entries)} entries")
            return entries
            
        except Exception as e:
            logger.error(f"[GC Scraper] Error scraping entries: {e}")
            return []
    
    def scrape_workouts(self) -> List[Dict[str, Any]]:
        """
        Scrape daily workouts (galoplar)
        """
        try:
            url = f"{GC_BASE}/site/gunluk-galoplar.html"
            logger.info("[GC Scraper] Scraping workouts...")
            
            response = get(url, referer=GC_BASE)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            workouts = []
            
            # Parse workout data
            tables = soup.find_all('table')
            for table in tables[:3]:
                rows = table.find_all('tr')[1:]
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        workout = {
                            "horse": cols[0].get_text(strip=True),
                            "time": cols[1].get_text(strip=True),
                            "distance": cols[2].get_text(strip=True),
                            "date": date.today().isoformat()
                        }
                        workouts.append(workout)
            
            logger.info(f"[GC Scraper] Scraped {len(workouts)} workouts")
            return workouts
            
        except Exception as e:
            logger.error(f"[GC Scraper] Error scraping workouts: {e}")
            return []

# Global instance
ganyancanavari_scraper = GanyancanavarScraper()
