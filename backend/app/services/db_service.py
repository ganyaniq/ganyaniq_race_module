from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URL, DB_NAME
from typing import Optional, List, Dict, Any
from datetime import datetime

class DatabaseService:
    """MongoDB database service"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
    
    async def connect(self):
        """Connect to MongoDB"""
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.db = self.client[DB_NAME]
        print(f"[Database] Connected to MongoDB: {DB_NAME}")
    
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("[Database] Closed MongoDB connection")
    
    # Race Program
    async def save_race_program(self, date: str, races: List[Dict[str, Any]]):
        """Save race program to database"""
        await self.db.race_programs.update_one(
            {"date": date},
            {"$set": {"date": date, "races": races, "updated_at": datetime.utcnow()}},
            upsert=True
        )
    
    async def get_race_program(self, date: str) -> Optional[Dict[str, Any]]:
        """Get race program from database"""
        return await self.db.race_programs.find_one({"date": date})
    
    # Race Results
    async def save_race_results(self, date: str, results: List[Dict[str, Any]]):
        """Save race results to database"""
        await self.db.race_results.update_one(
            {"date": date},
            {"$set": {"date": date, "results": results, "updated_at": datetime.utcnow()}},
            upsert=True
        )
    
    async def get_race_results(self, date: str) -> Optional[Dict[str, Any]]:
        """Get race results from database"""
        return await self.db.race_results.find_one({"date": date})
    
    # News
    async def save_news(self, news: Dict[str, Any]):
        """Save news article"""
        await self.db.news.insert_one({**news, "created_at": datetime.utcnow()})
    
    async def get_latest_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get latest news"""
        cursor = self.db.news.find().sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

# Global database service instance
db_service = DatabaseService()
