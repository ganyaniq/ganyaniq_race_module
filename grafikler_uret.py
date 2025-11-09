# grafikler_uret.py
import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("static/plots", exist_ok=True)

# === 1. ALFONSO FAVORİ SAFKAN BAŞARI ORANI ===
df_tahmin = pd.read_csv("data/alfonso_output.csv")
df_sonuc = pd.read_csv("data/yaris_sonuclari.csv")

# En çok önerilen 5 safkanı al
favori_safkanlar = df_tahmin["tahmin1"].value_counts().head(5).index.tolist()

basari_oranlari = {}
for safkan in favori_safkanlar:
    tahmin_edildi = df_tahmin[df_tahmin["tahmin1"] == safkan]
    kazandi = df_sonuc[df_sonuc["birinci"] == safkan]
    oran = round(len(kazandi) / len(tahmin_edildi) * 100, 2) if len(tahmin_edildi) > 0 else 0
    basari_oranlari[safkan] = oran

plt.figure(figsize=(8, 5))
plt.bar(basari_oranlari.keys(), basari_oranlari.values(), color='skyblue')
plt.ylabel("Başarı Oranı (%)")
plt.title("Alfonso'nun Favori Safkanlardaki Başarı Oranı")
plt.tight_layout()
plt.savefig("static/plots/alfonso_safkan_basarisi.png")
plt.close()

# === 2. ALFONSO İÇGÖRÜ NOTU ANALİZİ ===
df_icgoru = pd.read_csv("data/alfonso_icgoruler.csv")
puanlar = df_icgoru["icgoru_puani"]
plt.figure(figsize=(8, 5))
plt.hist(puanlar, bins=10, color='orange', edgecolor='black')
plt.title("Alfonso İçgörü Not Dağılımı")
plt.xlabel("İçgörü Puanı")
plt.ylabel("Frekans")
plt.tight_layout()
plt.savefig("static/plots/alfonso_icgoru_analiz.png")
plt.close()
