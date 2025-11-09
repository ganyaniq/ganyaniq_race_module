import matplotlib.pyplot as plt
import pandas as pd
from db.database import get_db
from db.models import Sonuc, Yarismaci
from sqlalchemy.orm import Session

def grafik_tahmin_performansi():
    db = next(get_db())
    query = db.query(Sonuc).all()

    kazananlar = {}
    for s in query:
        jokey = s.jokey
        if s.sira == 1:
            kazananlar[jokey] = kazananlar.get(jokey, 0) + 1

    df = pd.DataFrame(list(kazananlar.items()), columns=["Jokey", "Kazandigi_Kosu"])
    df_sorted = df.sort_values("Kazandigi_Kosu", ascending=False).head(10)

    plt.figure(figsize=(10,6))
    plt.bar(df_sorted["Jokey"], df_sorted["Kazandigi_Kosu"])
    plt.title("Son 10 Jokey - Kazanma Sayısı")
    plt.ylabel("Kazandığı Koşu")
    plt.xlabel("Jokey")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/grafikler/lyra_jokey_performans.png")
    plt.close()

    print("✅ LYRA: Jokey performans grafiği oluşturuldu.")
