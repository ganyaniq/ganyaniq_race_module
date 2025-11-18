from __future__ import annotations
import logging
import json
import os
from typing import List, Dict, Any, Optional
from datetime import date
import openai

logger = logging.getLogger(__name__)

# Use Emergent LLM Key
import os
EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY", "sk-emergent-cAa9a231b85044c413")
openai.api_key = EMERGENT_LLM_KEY
openai.api_base = "https://api.openai.com/v1"

class AlfonsoAI:
    """
    Alfonso AI - Ganyan Tahmin Uzmanı
    At yarışları için yapay zeka tabanlı tahmin sistemi
    """
    
    def __init__(self):
        self.model = "gpt-4o-mini"  # Cost-effective model
        self.max_predictions = 3  # Max 3 predictions per race
    
    async def analyze_race(self, race_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single race and provide predictions
        
        Args:
            race_data: Race information including horses, jockeys, track conditions
        
        Returns:
            Prediction with top 3 horses and analysis
        """
        try:
            hippodrome = race_data.get("hippodrome", "Unknown")
            race_no = race_data.get("race_no", 1)
            distance = race_data.get("distance", "1400m")
            track_type = race_data.get("type", "Kum")
            
            logger.info(f"[Alfonso AI] Analyzing race: {hippodrome} R{race_no}")
            
            # Create prompt for AI
            prompt = self._create_analysis_prompt(race_data)
            
            # Call OpenAI API
            response = await self._call_llm(prompt)
            
            # Parse response
            prediction = self._parse_prediction(response, race_data)
            
            return prediction
            
        except Exception as e:
            logger.error(f"[Alfonso AI] Error analyzing race: {e}")
            return self._generate_fallback_prediction(race_data)
    
    async def analyze_daily_program(self, races: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze all races in daily program
        
        Args:
            races: List of race data
        
        Returns:
            List of predictions for each race
        """
        predictions = []
        
        for race in races[:5]:  # Limit to 5 races to save costs
            try:
                prediction = await self.analyze_race(race)
                predictions.append(prediction)
            except Exception as e:
                logger.error(f"[Alfonso AI] Error in daily analysis: {e}")
        
        logger.info(f"[Alfonso AI] Generated {len(predictions)} predictions")
        return predictions
    
    def _create_analysis_prompt(self, race_data: Dict[str, Any]) -> str:
        """
        Create AI prompt for race analysis
        """
        hippodrome = race_data.get("hippodrome", "Unknown")
        race_no = race_data.get("race_no", 1)
        distance = race_data.get("distance", "1400m")
        track_type = race_data.get("type", "Kum")
        
        prompt = f"""Sen Alfonso, Türkiye'deki at yarışları için ganyan tahminleri yapan bir yapay zeka uzmanısın.

Yarış Bilgileri:
- Hipodrom: {hippodrome}
- Yarış No: {race_no}
- Mesafe: {distance}
- Pist Tipi: {track_type}

Görevin: Bu yarış için en çok kazanma şansı olan 3 atı tahmin et ve kısa bir analiz sun.

Yanıt formatı (JSON):
{{
  "predictions": [
    {{"horse_number": 3, "confidence": 85, "reason": "Güçlü form, iyi jokey"}},
    {{"horse_number": 7, "confidence": 75, "reason": "Mesafe uygun, geçmişte başarılı"}},
    {{"horse_number": 1, "confidence": 65, "reason": "Sürpriz aday, iyi antrör"}} 
  ],
  "analysis": "Kısa genel değerlendirme"
}}

Sadece JSON formatında yanıt ver, başka açıklama ekleme."""
        
        return prompt
    
    async def _call_llm(self, prompt: str) -> str:
        """
        Call OpenAI API with Emergent LLM Key
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Sen Alfonso, at yarışları tahmin uzmanısın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"[Alfonso AI] LLM API error: {e}")
            raise
    
    def _parse_prediction(self, llm_response: str, race_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse LLM response and structure prediction
        """
        try:
            # Try to parse JSON response
            # Remove markdown code blocks if present
            clean_response = llm_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.startswith("```"):
                clean_response = clean_response[3:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            
            prediction_data = json.loads(clean_response.strip())
            
            return {
                "race_info": {
                    "hippodrome": race_data.get("hippodrome"),
                    "race_no": race_data.get("race_no"),
                    "date": race_data.get("day")
                },
                "predictions": prediction_data.get("predictions", []),
                "analysis": prediction_data.get("analysis", ""),
                "model": "Alfonso AI",
                "confidence_level": "medium"
            }
            
        except Exception as e:
            logger.error(f"[Alfonso AI] Error parsing prediction: {e}")
            return self._generate_fallback_prediction(race_data)
    
    def _generate_fallback_prediction(self, race_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate fallback prediction when AI fails
        """
        return {
            "race_info": {
                "hippodrome": race_data.get("hippodrome"),
                "race_no": race_data.get("race_no"),
                "date": race_data.get("day")
            },
            "predictions": [
                {"horse_number": 1, "confidence": 60, "reason": "Otomatik tahmin"},
                {"horse_number": 3, "confidence": 55, "reason": "Otomatik tahmin"},
                {"horse_number": 5, "confidence": 50, "reason": "Otomatik tahmin"}
            ],
            "analysis": "AI analizi şu anda kullanılamıyor. Otomatik tahmin oluşturuldu.",
            "model": "Fallback",
            "confidence_level": "low"
        }

# Global Alfonso instance
alfonso_ai = AlfonsoAI()
