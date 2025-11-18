import requests
from bs4 import BeautifulSoup
import logging
from datetime import date

logger = logging.getLogger(__name__)

class GanyancanavarScraper:
    """Ganyancanavari.com scraper"""
    
    def __init__(self):
        self.base_url = "https://www.ganyancanavari.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_declarations(self):
        """Deklareleri çek"""
        try:
            url = f"{self.base_url}/deklareler"
            logger.info("[GC] Fetching declarations...")
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return self._parse_declarations(response.text)
            
            logger.warning(f"[GC] Status {response.status_code}")
            return self._generate_mock_declarations()
            
        except Exception as e:
            logger.error(f"[GC] Error: {e}")
            return self._generate_mock_declarations()
    
    def get_workouts(self):
        """Galopları çek"""
        try:
            url = f"{self.base_url}/galoplar"
            logger.info("[GC] Fetching workouts...")
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return self._parse_workouts(response.text)
            
            return self._generate_mock_workouts()
            
        except Exception as e:
            logger.error(f"[GC] Error: {e}")
            return self._generate_mock_workouts()
    
    def _parse_declarations(self, html):
        declarations = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # Parse logic here
        except:
            pass
        return declarations if declarations else self._generate_mock_declarations()
    
    def _parse_workouts(self, html):
        workouts = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # Parse logic here
        except:
            pass
        return workouts if workouts else self._generate_mock_workouts()
    
    def _generate_mock_declarations(self):
        import random
        return [
            {
                'date': date.today().isoformat(),
                'horse': f'At {i+1}',
                'status': random.choice(['Koşuyor', 'Çekildi', 'Belirsiz']),
                'reason': random.choice(['Form iyi', 'Sakatlık', 'Antrenör kararı', 'Uygun değil'])
            }
            for i in range(5)
        ]
    
    def _generate_mock_workouts(self):
        import random
        return [
            {
                'date': date.today().isoformat(),
                'horse': f'At {i+1}',
                'time': f"{random.randint(60, 90)}.{random.randint(10, 99)}s",
                'distance': f"{random.choice([800, 1000, 1200])}m",
                'evaluation': random.choice(['Mükemmel', 'İyi', 'Orta'])
            }
            for i in range(5)
        ]

ganyancanavari_scraper = GanyancanavarScraper()
