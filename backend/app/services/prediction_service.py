from __future__ import annotations
import logging
from typing import List, Dict, Any
from datetime import datetime
from app.ai.alfonso import alfonso_ai
from app.services.db_service import db_service

logger = logging.getLogger(__name__)

class PredictionService:
    """Service for managing AI predictions"""
    
    async def generate_daily_predictions(self, date_str: str) -> List[Dict[str, Any]]:
        """
        Generate predictions for all races in a day
        
        Args:
            date_str: Date in YYYY-MM-DD format
        
        Returns:
            List of predictions
        """
        try:
            logger.info(f"[Prediction Service] Generating predictions for {date_str}")
            
            # Get race program from database
            program_data = await db_service.get_race_program(date_str)
            
            if not program_data or "races" not in program_data:
                logger.warning(f"[Prediction Service] No races found for {date_str}")
                return []
            
            races = program_data["races"]
            
            # Generate predictions using Alfonso AI
            predictions = await alfonso_ai.analyze_daily_program(races)
            
            # Save predictions to database
            if predictions:
                await db_service.db.predictions.update_one(
                    {"date": date_str},
                    {
                        "$set": {
                            "date": date_str,
                            "predictions": predictions,
                            "generated_at": datetime.utcnow(),
                            "model": "Alfonso AI"
                        }
                    },
                    upsert=True
                )
                logger.info(f"[Prediction Service] Saved {len(predictions)} predictions")
            
            return predictions
            
        except Exception as e:
            logger.error(f"[Prediction Service] Error generating predictions: {e}")
            return []
    
    async def get_race_prediction(self, date_str: str, hippodrome: str, race_no: int) -> Dict[str, Any]:
        """
        Get prediction for a specific race
        """
        try:
            prediction_data = await db_service.db.predictions.find_one({"date": date_str})
            
            if not prediction_data:
                return {}
            
            # Find specific race prediction
            for pred in prediction_data.get("predictions", []):
                race_info = pred.get("race_info", {})
                if (race_info.get("hippodrome") == hippodrome and 
                    race_info.get("race_no") == race_no):
                    return pred
            
            return {}
            
        except Exception as e:
            logger.error(f"[Prediction Service] Error getting prediction: {e}")
            return {}

# Global service instance
prediction_service = PredictionService()
