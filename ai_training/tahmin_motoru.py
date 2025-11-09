# tahmin_motoru.py
import pickle
from ai_training.model_train import load_model
from database import get_db_session
from models import Yarismaci, Tahmin
from datetime import datetime

class TahminMotoru:
    def __init__(self, model_path="ai_training/model.pkl"):
        self.model = load_model(model_path)
        self.db = get_db_session()

    def tahmin_yap(self, yarismaci_id):
        # Yarışmacı bilgilerini çek
        yarismaci = self.db.query(Yarismaci).filter(Yarismaci.id == yarismaci_id).first()
        if not yarismaci:
            raise ValueError("Yarışmacı bulunamadı.")
        
        # Özellikler oluştur
        features = self.prepare_features(yarismaci)
        
        # Model ile tahmin yap
        prediction = self.model.predict([features])[0]
        
        # Tahmini kaydet
        tahmin = Tahmin(
            yarismaci_id=yarismaci_id,
            tahmin_degeri=prediction,
            tarih=datetime.utcnow()
        )
        self.db.add(tahmin)
        self.db.commit()
        return prediction

    def prepare_features(self, yarismaci):
        # Örnek: atın yaş, koşu sayısı, son derecesi gibi özellikleri dön
        return [
            yarismaci.yas,
            yarismaci.kosu_sayisi,
            yarismaci.son_derece
        ]
