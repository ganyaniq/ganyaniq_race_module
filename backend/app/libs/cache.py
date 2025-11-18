from functools import lru_cache
from datetime import datetime, timedelta

class SimpleCache:
    """Simple in-memory cache"""
    def __init__(self):
        self._cache = {}
    
    def get(self, key):
        if key in self._cache:
            data, expiry = self._cache[key]
            if datetime.now() < expiry:
                return data
            del self._cache[key]
        return None
    
    def set(self, key, value, ttl_seconds=300):
        expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache[key] = (value, expiry)
    
    def clear(self):
        self._cache.clear()

cache = SimpleCache()
