import requests
from bs4 import BeautifulSoup

def fetch_kategori_data(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    for item in soup.select('.kategori-item'):
        title = item.get_text(strip=True)
        data.append(title)
    return data
