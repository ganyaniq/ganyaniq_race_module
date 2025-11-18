from datetime import date
import random

class AdditionalDataService:
    def get_probables(self, target_date=None):
        """Muhtemel oranlar"""
        if not target_date:
            target_date = date.today()
        
        probables = []
        for i in range(5):
            prob = {
                'day': target_date.isoformat(),
                'hippodrome': ['İSTANBUL', 'ANKARA', 'İZMİR'][i % 3],
                'race_no': i + 1,
                'horses': [
                    {'number': 1, 'probable': round(2.5 + random.random() * 2, 2)},
                    {'number': 2, 'probable': round(3.0 + random.random() * 2, 2)},
                    {'number': 3, 'probable': round(2.8 + random.random() * 2, 2)},
                    {'number': 4, 'probable': round(4.0 + random.random() * 3, 2)},
                    {'number': 5, 'probable': round(3.5 + random.random() * 2, 2)},
                ]
            }
            probables.append(prob)
        return probables
    
    def get_weather_conditions(self):
        """Hava ve pist durumları"""
        conditions = [
            {
                'hippodrome': 'İSTANBUL',
                'weather': 'Açık',
                'temperature': '18°C',
                'track_condition': 'İyi',
                'humidity': '%65'
            },
            {
                'hippodrome': 'ANKARA',
                'weather': 'Bulutlu',
                'temperature': '15°C',
                'track_condition': 'Orta',
                'humidity': '%70'
            },
            {
                'hippodrome': 'İZMİR',
                'weather': 'Açık',
                'temperature': '22°C',
                'track_condition': 'Mükemmel',
                'humidity': '%55'
            }
        ]
        return conditions
    
    def get_news(self):
        """Güncel haberler"""
        news = [
            {
                'title': 'İstanbul\'da heyecanlı yarış günü bekleniyor',
                'source': 'TJK',
                'date': date.today().isoformat(),
                'summary': 'Bugün İstanbul hipodromunda 8 heyecanlı yarış koşulacak.'
            },
            {
                'title': 'Şampiyon jokey Ahmet Çelik yeni rekor peşinde',
                'source': 'At Yarışları',
                'date': date.today().isoformat(),
                'summary': 'Sezonun en başarılı jokeyi bu hafta sonu tarih yazabilir.'
            },
            {
                'title': 'Yeni nesil atlar yarış pistlerinde',
                'source': 'TJK',
                'date': date.today().isoformat(),
                'summary': 'Bu sezon yetiştirilen genç atlar ilk yarışlarına çıkıyor.'
            }
        ]
        return news

additional_data_service = AdditionalDataService()
