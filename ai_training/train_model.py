# ai_training/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# 1. Veriyi yükle
df = pd.read_csv("ai_training/training_data.csv")

# 2. Feature ve target ayır
X = df.drop(columns=["kazanan"])  # kazanan = hedef değişken
y = df["kazanan"]

# 3. Eğitim-test ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Modeli eğit
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Doğruluk değerlendirme
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"🎯 Model doğruluk oranı: {accuracy * 100:.2f}%")

# 6. Kaydet
joblib.dump(model, "ai_training/alfonso_model.pkl")
