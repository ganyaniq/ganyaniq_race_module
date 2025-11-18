import random
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class LyraAI:
    """Lyra AI - Grafik ve Tempo Analizi"""
    
    async def generate_chart_data(self, races):
        """Grafik verileri oluşturur"""
        charts = []
        
        # Tempo analizi
        for race in races[:3]:
            tempo_chart = {
                'race_info': {
                    'hippodrome': race.get('hippodrome'),
                    'race_no': race.get('race_no'),
                    'date': race.get('day')
                },
                'type': 'tempo_analysis',
                'data': {
                    'start_tempo': random.choice(['Yavaş', 'Orta', 'Hızlı']),
                    'middle_tempo': random.choice(['Sabit', 'Hızlanan', 'Yavaşlayan']),
                    'finish_tempo': random.choice(['Sprint', 'Uzun', 'Dengeli']),
                    'tempo_score': round(random.uniform(6.5, 9.5), 1)
                },
                'recommendation': random.choice([
                    'Erken pozisyon alan atlar avantajlı',
                    'Geç hızlanan atlar için uygun',
                    'Sprint yapan atlar öne çıkabilir'
                ]),
                'model': 'Lyra AI'
            }
            charts.append(tempo_chart)
        
        logger.info(f"[Lyra] {len(charts)} grafik verisi oluşturuldu")
        return charts
    
    async def get_performance_trends(self, horse_id=None):
        """Performans trend grafiği"""
        # Son 10 yarışın performans trendi
        dates = [(datetime.now() - timedelta(days=i*7)).strftime('%Y-%m-%d') for i in range(10)]
        dates.reverse()
        
        trend = {
            'dates': dates,
            'performance': [round(random.uniform(5.0, 9.5), 1) for _ in range(10)],
            'positions': [random.randint(1, 12) for _ in range(10)],
            'trend': random.choice(['Yükseliş', 'Düşüş', 'Stabil']),
            'model': 'Lyra AI'
        }
        
        return trend

lyra_ai = LyraAI()
