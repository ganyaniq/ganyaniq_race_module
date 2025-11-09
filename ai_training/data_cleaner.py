import pandas as pd

def temizle_veri(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Boş verileri temizler
    - Sayısal olmayan sütunları tespit eder
    - Aykırı değerleri filtreler (isteğe bağlı)
    """
    print("🧼 Temizlik başlatıldı...")

    # 1. Boşlukları kaldır
    df = df.dropna()
    print(f"✅ Boşluklar temizlendi. Kalan satır sayısı: {len(df)}")

    # 2. Sadece sayısal sütunları al (Alfonso için uygun yapı)
    sayisal_sutunlar = df.select_dtypes(include=['int64', 'float64']).columns
    df = df[sayisal_sutunlar]
    print(f"🔢 Sayısal sütunlar kaldı: {list(sayisal_sutunlar)}")

    # 3. (İsteğe bağlı) Negatif veya saçma değerleri temizle
    if 'yas' in df.columns:
        df = df[df['yas'] > 0]

    return df
