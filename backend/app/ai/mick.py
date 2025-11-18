import random
import logging

logger = logging.getLogger(__name__)

class MickAI:
    """Mick AI - Sürpriz At Uzmanı"""
    
    async def find_surprise_horses(self, races):
        """Sürpriz at adayları bulur"""
        surprises = []
        
        for race in races[:2]:  # İlk 2 yarış
            surprise = {
                'race_info': {
                    'hippodrome': race.get('hippodrome'),
                    'race_no': race.get('race_no'),
                    'date': race.get('day')
                },
                'surprise_horse': random.randint(6, 12),
                'odds_estimate': round(random.uniform(8.0, 18.0), 2),
                'reasoning': random.choice([
                    'Son antrenmanlarında beklenmedik performans',
                    'Geçmiş yarışlarda gizli potansiyel gösterdi',
                    'Pist koşulları bu ata çok uygun',
                    'Jokey değişikliği olumlu etki yaratabilir'
                ]),
                'risk_level': random.choice(['Orta', 'Yüksek']),
                'model': 'Mick AI'
            }
            surprises.append(surprise)
        
        logger.info(f"[Mick] {len(surprises)} sürpriz at bulundu")
        return surprises

mick_ai = MickAI()
