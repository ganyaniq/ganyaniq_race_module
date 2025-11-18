from __future__ import annotations
import re
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from app.libs.net_client import get
import logging

logger = logging.getLogger(__name__)

TJK_BASE = "https://www.tjk.org"
TJK_REFERER = "https://www.tjk.org/tr/yarissever"

class TJKScraper:
    """TJK web scraper with anti-ban measures"""
    
    def __init__(self):
        self.session_referer = TJK_REFERER
    
    def scrape_daily_program(self, target_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """
        Scrape daily race program from TJK
        Returns list of races with basic info
        """
        if target_date is None:
            target_date = date.today()
        
        try:
            url = f"{TJK_BASE}/tr/yarissever/info/page/gunlukyarisprogrami"
            logger.info(f"Scraping TJK daily program for {target_date}...")
            
            # Make request with referer
            response = get(url, referer=self.session_referer)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            races = []
            
            # Parse race program table
            # Note: TJK uses dynamic content, this is a simplified parser
            # Real implementation would need to handle JavaScript-rendered content
            
            tables = soup.find_all('table', class_='table')
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 5:
                        race = {
                            "day": target_date.isoformat(),
                            "hippodrome": cols[0].get_text(strip=True),
                            "race_no": int(cols[1].get_text(strip=True)) if cols[1].get_text(strip=True).isdigit() else 0,
                            "distance": cols[2].get_text(strip=True),
                            "type": cols[3].get_text(strip=True),
                            "start_time": cols[4].get_text(strip=True)
                        }
                        races.append(race)
            
            logger.info(f"Scraped {len(races)} races for {target_date}")
            return races
            
        except Exception as e:
            logger.error(f"Error scraping TJK program: {e}")
            return []
    
    def scrape_daily_results(self, target_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """
        Scrape daily race results from TJK
        Returns list of race results
        """
        if target_date is None:
            target_date = date.today()
        
        try:
            url = f"{TJK_BASE}/tr/yarissever/info/page/gunlukyarissonuclari"
            logger.info(f"Scraping TJK daily results for {target_date}...")
            
            response = get(url, referer=self.session_referer)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            
            # Parse results table
            tables = soup.find_all('table', class_='table')
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 6:
                        result = {
                            "day": target_date.isoformat(),
                            "hippodrome": cols[0].get_text(strip=True),
                            "race_no": int(cols[1].get_text(strip=True)) if cols[1].get_text(strip=True).isdigit() else 0,
                            "first": self._extract_number(cols[2].get_text(strip=True)),
                            "second": self._extract_number(cols[3].get_text(strip=True)),
                            "ganyan": self._extract_float(cols[4].get_text(strip=True)),
                        }
                        results.append(result)
            
            logger.info(f"Scraped {len(results)} results for {target_date}")
            return results
            
        except Exception as e:
            logger.error(f"Error scraping TJK results: {e}")
            return []
    
    def _extract_number(self, text: str) -> Optional[int]:
        """Extract first number from text"""
        match = re.search(r'\d+', text)
        return int(match.group()) if match else None
    
    def _extract_float(self, text: str) -> Optional[float]:
        """Extract float from text"""
        try:
            # Remove currency symbols and convert to float
            clean = re.sub(r'[^0-9.,]', '', text)
            clean = clean.replace(',', '.')
            return float(clean) if clean else None
        except:
            return None

# Global scraper instance
tjk_scraper = TJKScraper()
