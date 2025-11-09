import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def egit_alfonso_modeli(veri_yolu, model_yolu):
    # Veriyi oku
    veri = pd.read_csv(veri_yolu)

    # Özellikler ve etiket
    X = veri.drop(columns=['kazandi'])
    y = veri['kazandi']

    # Modeli oluştur ve eğit
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Modeli kaydet
    os.makedirs(os.path.dirname(model_yolu), exist_ok=True)
    joblib.dump(model, model_yolu)

    print(f"✅ Alfonso modeli eğitildi ve kaydedildi → {model_yolu}")

if __name__ == "__main__":
    # Varsayılan yol ayarları (gerekirse değiştirilebilir)
    egit_alfonso_modeli(
        veri_yolu="data/train_set.csv",
        model_yolu="ai/checkpoints/model_checkpoint_alfonso_25haz.pkl"
    )
