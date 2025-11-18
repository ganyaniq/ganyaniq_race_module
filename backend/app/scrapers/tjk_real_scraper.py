import requests
import logging
from datetime import date, datetime
from bs4 import BeautifulSoup
import json

logger = logging.getLogger(__name__)

class TJKRealScraper:
    """Gerçek TJK verilerini çeker"""
    
    def __init__(self):
        self.base_url = "https://www.tjk.org"
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
    
    def _get_session(self):
        """Ana sayfadan session oluştur (404 engeli için)"""
        if self.session is None:
            self.session = requests.Session()
            self.session.headers.update(self.headers)
            
            try:
                # 1. Ana sayfaya git (session/cookie al)
                logger.info("[TJK Real] Ana sayfadan session alınıyor...")
                home_response = self.session.get(self.base_url, timeout=10)
                
                if home_response.status_code == 200:
                    logger.info("[TJK Real] Session başarılı!")
                    # Referer'ı güncelle
                    self.session.headers['Referer'] = self.base_url
                else:
                    logger.warning(f"[TJK Real] Home page status: {home_response.status_code}")
            except Exception as e:
                logger.error(f"[TJK Real] Session error: {e}")
        
        return self.session
    
    def get_daily_program(self, target_date=None):
        """Günlük yarış programını çek"""
        if not target_date:
            target_date = date.today()
        
        try:
            # Session al (ana sayfadan)
            session = self._get_session()
            
            # 2. Alt sayfaya git
            url = f"{self.base_url}/TR/YarisSever/Query/Page/GunlukYarisProgrami"
            
            logger.info(f"[TJK Real] Fetching program for {target_date}")
            
            response = session.get(url, timeout=10)
            
            if response.status_code == 200:
                races = self._parse_program(response.text, target_date)
                logger.info(f"[TJK Real] Found {len(races)} races")
                return races
            else:
                logger.warning(f"[TJK Real] Status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"[TJK Real] Error: {e}")
            return []
    
    def get_daily_results(self, target_date=None):
        """Günlük yarış sonuçlarını çek"""
        if not target_date:
            target_date = date.today()
        
        try:
            # Session al (ana sayfadan)
            session = self._get_session()
            
            # Alt sayfaya git
            url = f"{self.base_url}/TR/YarisSever/Query/Page/GunlukYarisSonuclari"
            
            logger.info(f"[TJK Real] Fetching results for {target_date}")
            
            response = session.get(url, timeout=10)
            
            if response.status_code == 200:
                results = self._parse_results(response.text, target_date)
                logger.info(f"[TJK Real] Found {len(results)} results")
                return results
            else:
                logger.warning(f"[TJK Real] Status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"[TJK Real] Error: {e}")
            return []
    
    def _parse_program(self, html, target_date):
        """HTML'den program parse et"""
        races = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # TJK'nın tablo yapısını parse et
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        try:
                            race = {
                                'day': target_date.isoformat(),
                                'hippodrome': cols[0].get_text(strip=True) or 'İSTANBUL',
                                'race_no': int(cols[1].get_text(strip=True)) if cols[1].get_text(strip=True).isdigit() else 1,
                                'distance': cols[2].get_text(strip=True) or '1400m',
                                'type': cols[3].get_text(strip=True) or 'Kum',
                                'start_time': cols[4].get_text(strip=True) if len(cols) > 4 else '13:00'
                            }
                            races.append(race)
                        except:
                            continue
            
        except Exception as e:
            logger.error(f"[TJK Real] Parse error: {e}")
        
        return races
    
    def _parse_results(self, html, target_date):
        """HTML'den sonuçları parse et"""
        results = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')[1:]
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 5:
                        try:
                            result = {
                                'day': target_date.isoformat(),
                                'hippodrome': cols[0].get_text(strip=True) or 'İSTANBUL',
                                'race_no': int(cols[1].get_text(strip=True)) if cols[1].get_text(strip=True).isdigit() else 1,
                                'first': int(cols[2].get_text(strip=True)) if cols[2].get_text(strip=True).isdigit() else 1,
                                'second': int(cols[3].get_text(strip=True)) if cols[3].get_text(strip=True).isdigit() else 2,
                                'ganyan': cols[4].get_text(strip=True) or '0.00'
                            }
                            results.append(result)
                        except:
                            continue
            
        except Exception as e:
            logger.error(f"[TJK Real] Parse error: {e}")
        
        return results

tjk_real_scraper = TJKRealScraper()
