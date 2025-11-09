
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib

def train_model():
    csv_path = "data/yeni_kosular_guncel.csv"
    print("🔍 Veri dosyası yükleniyor...")

    df = pd.read_csv(csv_path)
    print("✅ Veri başarıyla yüklendi.")

    # Kategorik verileri dönüştür
    le_dict = {}
    for column in df.columns:
        if df[column].dtype == 'object':
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column].astype(str))
            le_dict[column] = le

    if "target" not in df.columns:
        raise ValueError("❌ 'target' sütunu veri setinde bulunamadı!")

    X = df.drop(columns=["target"])
    y = df["target"]

    print("🧠 Model eğitiliyor...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    print("✅ Model başarıyla eğitildi.")

    joblib.dump(model, "alfonso_model.pkl")
    print("💾 Model 'alfonso_model.pkl' olarak kaydedildi.")
