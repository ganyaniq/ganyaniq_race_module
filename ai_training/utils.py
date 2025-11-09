import pandas as pd

def kontrol_et_bosluklar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Boş hücre sayısını sütun bazında gösterir.
    """
    print("📊 Sütun bazında boşluk kontrolü:")
    print(df.isnull().sum())
    return df

def kolon_kontrol(df: pd.DataFrame, gerekli_kolonlar: list) -> bool:
    """
    Gerekli kolonların veri içinde olup olmadığını kontrol eder.
    """
    eksikler = [kolon for kolon in gerekli_kolonlar if kolon not in df.columns]
    if eksikler:
        print(f"❗Eksik kolonlar: {eksikler}")
        return False
    print("✅ Tüm kolonlar mevcut.")
    return True

def encode_et(df: pd.DataFrame, kategorik_kolonlar: list) -> pd.DataFrame:
    """
    Kategorik değişkenleri sayısal verilere çevirir.
    """
    for kolon in kategorik_kolonlar:
        df[kolon] = df[kolon].astype('category').cat.codes
    return df
