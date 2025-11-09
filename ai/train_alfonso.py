import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_alfonso_model(csv_path, model_output_path):
    df = pd.read_csv(csv_path)

    X = df.drop(columns=['kazandi'])
    y = df['kazandi']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, model_output_path)
    print(f"[Alfonso] Model eğitildi ve kaydedildi → {model_output_path}")

if __name__ == "__main__":
    train_alfonso_model("data/train_set.csv", "ai/checkpoints/model_checkpoint_2406_v1.pkl")
