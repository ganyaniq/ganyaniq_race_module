import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib
import os
from datetime import datetime

def temizle_veri(df):
    df = df.dropna()
    return df

def alfonso_model_olustur(X, y):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def egitim_skorlari(model, X, y):
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    return accuracy, f1

def modeli_kaydet(model, model_yolu):
    os.makedirs(os.path.dirname(model_yolu), exist_ok=True)
    joblib.dump(model, model_yolu)

def log_egitim_bilgileri(log_path, accuracy, f1, model_yolu):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'a', encoding='utf-8') as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{now} - Model: {model_yolu} - Accuracy: {accuracy:.4f}, F1: {f1:.4f}\n")

def alfonso_egitim_pipeline(csv_yolu, model_yolu, log_yolu=None):
    print(f"📦 Veri yükleniyor: {csv_yolu}")
    df = pd.read_csv(csv_yolu)

    print("🧼 Veri temizleniyor...")
    df = temizle_veri(df)

    print("🔬 Özellik ve etiket ayrıştırılıyor...")
    X = df.drop(columns=['kazandi'])
    y = df['kazandi']

    print("🤖 Model eğitiliyor...")
    model = alfonso_model_olustur(X, y)

    print("📊 Performans hesaplanıyor...")
    acc, f1 = egitim_skorlari(model, X, y)
    print(f"✅ Doğruluk (Accuracy): {acc:.4f}, F1 Skoru: {f1:.4f}")

    print(f"💾 Model kaydediliyor: {model_yolu}")
    modeli_kaydet(model, model_yolu)

    if log_yolu:
        print(f"🗒️ Eğitim loglanıyor → {log_yolu}")
        log_egitim_bilgileri(log_yolu, acc, f1, model_yolu)

    print("🚀 Eğitim tamamlandı!")

# Örnek kullanım
if __name__ == "__main__":
    alfonso_egitim_pipeline(
        csv_yolu="data/train_set.csv",
        model_yolu="ai/checkpoints/alfonso_model_25haz.pkl",
        log_yolu="logs/egitim_log.txt"
    )
