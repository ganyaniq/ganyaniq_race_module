
import os
import shutil
from datetime import datetime

def yedekle():
    kaynak_klasor = "."
    hedef_klasor = "./yedekler"
    os.makedirs(hedef_klasor, exist_ok=True)

    tarih = datetime.now().strftime("%Y%m%d_%H%M")
    yedek_dosya = os.path.join(hedef_klasor, f"ganyaniq_yedek_{tarih}")

    try:
        shutil.make_archive(yedek_dosya, 'zip', kaynak_klasor)
        print(f"✅ Yedek alındı: {yedek_dosya}.zip")
    except Exception as e:
        print(f"❌ Yedekleme hatası: {e}")

if __name__ == "__main__":
    yedekle()
