import pandas as pd
import os
from datetime import datetime

def sec_gecmis_yarislari(df: pd.DataFrame) -> pd.DataFrame:
    """
    Etiketli veri (kazanan belli) → Eğitim seti için
    """
    df = df.dropna(subset=['kazandi'])  # Etiketi olmayanları at
    df = df[df['kazandi'].isin([0, 1])]
    return df

def sec_bugunku_yarislari(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bugün koşulacak yarışlardan tahmin girdisi
    """
    df = df[df['kazandi'].isnull()]
    df = df.drop(columns=['kazandi'], errors='ignore')
    return df

def kaydet(df: pd.DataFrame, yol: str):
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    df.to_csv(yol, index=False)
    print(f"💾 Kaydedildi: {yol} ({len(df)} satır)")

def uret_veri_kumesi(tum_veri_csv="data/yarislardaki_tum_atlar.csv"):
    print(f"📥 Tüm veri okunuyor: {tum_veri_csv}")
    df = pd.read_csv(tum_veri_csv)

    print("🔍 Geçmiş yarışlar ayrıştırılıyor...")
    egitim_df = sec_gecmis_yarislari(df)
    kaydet(egitim_df, "data/train_set.csv")

    print("🔍 Bugünkü koşular ayrıştırılıyor...")
    tahmin_df = sec_bugunku_yarislari(df)
    kaydet(tahmin_df, "data/yeni_koşular.csv")

    print("🎯 Veri üretim işlemi tamamlandı.")

# Test
if __name__ == "__main__":
    uret_veri_kumesi()
