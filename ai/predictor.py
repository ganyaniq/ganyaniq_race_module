import pandas as pd
import joblib

def load_model(model_path):
    return joblib.load(model_path)

def predict_from_input(input_data, model):
    df = pd.DataFrame([input_data])
    prediction = model.predict(df)
    prediction_proba = model.predict_proba(df)
    return prediction[0], prediction_proba[0]

if __name__ == "__main__":
    model = load_model("ai/checkpoints/model_checkpoint_2406_v1.pkl")
    ornek_girdi = {
        'yas': 4,
        'jokey_puani': 85,
        'son_3_yaris': 2,
        'agf': 12.8,
        'galop_puani': 74
    }

    tahmin, olasiliklar = predict_from_input(ornek_girdi, model)
    print(f"Tahmin edilen safkan: {tahmin}")
    print("Olasılıklar:", olasiliklar)
