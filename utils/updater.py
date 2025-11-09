import os
import shutil

def get_last_kosu_id(path="templates/kosu"):
    ids = [f.split(".")[0] for f in os.listdir(path) if f.endswith(".html") and f.split(".")[0].isdigit()]
    return sorted(ids)[-1] if ids else None

def guncel_sayfalari_guncelle():
    last_id = get_last_kosu_id()
    if last_id:
        kosu_src = f"templates/kosu/{last_id}.html"
        sonuc_src = f"templates/sonuclar/{last_id}.html"
        kosu_dst = "templates/kosu/program.html"
        sonuc_dst = "templates/sonuclar/sonuc.html"

        try:
            if os.path.exists(kosu_src):
                shutil.copyfile(kosu_src, kosu_dst)
            if os.path.exists(sonuc_src):
                shutil.copyfile(sonuc_src, sonuc_dst)
        except Exception as e:
            print(f"[HATA] Güncelleme işlemi başarısız: {e}")
