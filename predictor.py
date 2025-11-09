import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

model = joblib.load("alfonso_model.pkl")

def predict_from_csv(csv_path):
    df = pd.read_csv(csv_path)

    # Kategorik (string) sütunları sayısala dönüştür
    for col in df.columns:
        if df[col].dtype == "object":
            encoder = LabelEncoder()
            df[col] = encoder.fit_transform(df[col].astype(str))

    predictions = model.predict(df)
    probabilities = model.predict_proba(df)
    return predictions.tolist(), probabilities.tolist()
