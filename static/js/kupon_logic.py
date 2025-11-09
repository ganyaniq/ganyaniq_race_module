
def icgoru_notu_uret(kosu):
    """
    Alfonso'nun AI tahminlerine göre koşu bazlı içgörü üretir.
    """

    tahminler = kosu.get("tahmin", [])
    icgoru = ""

    favori = tahminler[0] if tahminler else {}
    oran = float(favori.get("oran", "0").replace(",", ".")) if favori.get("oran") else 0

    if oran > 5:
        icgoru = "Favori atın oranı yüksek. Sürpriz yaşanabilir."
    elif tahminler and len(tahminler) >= 3:
        s3 = tahminler[2]
        s3_oran = float(s3.get("oran", "0").replace(",", ".")) if s3.get("oran") else 0
        if s3_oran < 6:
            icgoru = "İlk üçteki atların oranları düşük. İkili/üçlü oyunlar için ideal."
    elif favori.get("isim", "").lower().startswith("yorgun") or "dinlenme" in favori.get("isim", "").lower():
        icgoru = "Favori at dinlenme sonrası ilk kez koşuyor. Dikkatli olunmalı."
    else:
        icgoru = "Favori sağlam görünüyor. Risk düşük."

    return icgoru
