import requests
from bs4 import BeautifulSoup
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; GANYANIQBot/1.0; +https://ganyaniq.com/bot)"
}

def fetch_handikap_puanlari(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        puanlar = []
        for row in soup.select('table.handikap tbody tr'):
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            puanlar.append(cols)
        time.sleep(random.uniform(1, 3))  # Ban riskini azaltmak için rastgele bekleme
        return puanlar
    except Exception as e:
        # Hata loglama mekanizmasına entegre edilmelidir
        print(f"Handikap veri çekme hatası: {e}")
        return []
