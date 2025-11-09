import pandas as pd
from predictor import alfonso_tahmin_et

# 🔧 Ayarlar
model_yolu = "ai/checkpoints/alfonso_model_25haz.pkl"
veri_yolu = "data/yeni_koşular.csv"

print(f"📥 Veri yükleniyor: {veri_yolu}")
veri = pd.read_csv(veri_yolu)

# Eğer veri etiket içeriyorsa (örn. 'kazandi'), onu kaldır
if 'kazandi' in veri.columns:
    veri = veri.drop(columns=['kazandi'])

# 🧠 Tahminleri al
print("🔮 Alfonso tahmin ediyor...")
tahminler = alfonso_tahmin_et(model_yolu, veri)

# 📊 Sonuçları göster
sonuc = pd.concat([veri, tahminler], axis=1)
print("✅ Tahmin tamamlandı. Örnek çıktı:")
print(sonuc.head())

# Kaydet
sonuc.to_csv("data/alfonso_tahmin_sonuclari.csv", index=False)
print("📁 Tahmin çıktısı kaydedildi → data/alfonso_tahmin_sonuclari.csv")
