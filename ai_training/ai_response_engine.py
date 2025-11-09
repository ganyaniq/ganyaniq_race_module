# 📁 MODÜL: ai_response_engine.py
# 🧾 AÇIKLAMA: Alfonso AI'nın tahmin verilerini işleyip dışa aktarır

import pickle
import json
from ai_training.model_train import preprocess_input

MODEL_PATH = "ai_training/model.pkl"


def yukle_model():
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        print(f"❌ Model yüklenemedi: {e}")
        return None


def tahmin_yap(girdi_verisi):
    """
    Girdi verisini alır, ön işler ve Alfonso tahmini döner
    :param girdi_verisi: dict formatında veriler
    :return: tahmin sonucu (dict)
    """
    model = yukle_model()
    if not model:
        return {"hata": "Model yüklenemedi."}

    try:
        X = preprocess_input(girdi_verisi)
        tahmin = model.predict(X)
        olasilik = model.predict_proba(X)

        return {
            "tahmin": tahmin.tolist(),
            "olasilik": olasilik.tolist()
        }
    except Exception as e:
        return {"hata": f"Tahmin yapılamadı: {e}"}


# Örnek veri:
# veri = {"yas": 4, "mesafe": 1600, "kategori": "KV-6"}
# print(tahmin_yap(veri))
