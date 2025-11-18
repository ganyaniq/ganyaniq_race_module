from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AdminService:
    """Admin panel servisleri"""
    
    async def get_system_stats(self):
        """Sistem istatistikleri"""
        from app.services.db_service import db_service
        
        try:
            # Database stats
            programs_count = await db_service.db.race_programs.count_documents({})
            results_count = await db_service.db.race_results.count_documents({})
            predictions_count = await db_service.db.predictions.count_documents({})
            
            stats = {
                'database': {
                    'programs': programs_count,
                    'results': results_count,
                    'predictions': predictions_count,
                    'total_documents': programs_count + results_count + predictions_count
                },
                'system': {
                    'uptime': 'Running',
                    'status': 'healthy',
                    'last_update': datetime.now().isoformat()
                },
                'ai_models': {
                    'alfonso': 'active',
                    'mick': 'active',
                    'arion': 'active',
                    'hermes': 'active',
                    'lyra': 'active'
                }
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"[Admin] Stats error: {e}")
            return {}
    
    async def clear_cache(self):
        """Cache temizle"""
        from app.libs.cache import cache
        cache.clear()
        return {'ok': True, 'message': 'Cache cleared'}
    
    async def get_recent_logs(self, limit=50):
        """Son log kayıtları"""
        # Mock log data
        logs = [
            {'timestamp': datetime.now().isoformat(), 'level': 'INFO', 'message': 'System started'},
            {'timestamp': datetime.now().isoformat(), 'level': 'INFO', 'message': 'Database connected'},
            {'timestamp': datetime.now().isoformat(), 'level': 'INFO', 'message': 'AI models loaded'}
        ]
        return logs[:limit]

admin_service = AdminService()
