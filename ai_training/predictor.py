import pandas as pd
import joblib
import os

def alfonso_tahmin_et(model_yolu: str, veri: pd.DataFrame) -> pd.Series:
    """
    Verilen model ile tahmin üretir.
    """
    if not os.path.exists(model_yolu):
        raise FileNotFoundError(f"❗ Model bulunamadı: {model_yolu}")

    print(f"📦 Model yükleniyor: {model_yolu}")
    model = joblib.load(model_yolu)

    print("🤖 Tahmin üretiliyor...")
    tahminler = model.predict(veri)

    return pd.Series(tahminler, name="alfonso_tahmin")

# Örnek kullanım
if __name__ == "__main__":
    veri_yolu = "data/yeni_koşular.csv"
    model_yolu = "ai/checkpoints/alfonso_model_25haz.pkl"

    veri = pd.read_csv(veri_yolu)
    tahmin = alfonso_tahmin_et(model_yolu, veri)

    sonuc = pd.concat([veri, tahmin], axis=1)
    print(sonuc.head())
