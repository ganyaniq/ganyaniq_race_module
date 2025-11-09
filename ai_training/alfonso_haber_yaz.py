# 📁 MODÜL: alfonso_haber_yaz.py
# 🧾 AÇIKLAMA: Alfonso’nun tahmin ve sonuçlarını haber formatına çevirir, linkli özet haber oluşturur

from datetime import datetime
import sqlite3


def alfonso_tahmin_haberi_olustur(kosu_id, tarih, baslik_etiketi, alfonso_slug):
    """
    Alfonso AI tarafından yapılan tahminin özet haberini oluşturur.
    Haber detayları sistemde yer almaz, yalnızca tahmin sayfasına yönlendirir.
    """
    baslik = f"Alfonso’dan {baslik_etiketi} Tahmini - {tarih}"
    ozet = f"Alfonso, {tarih} tarihli {baslik_etiketi} için özel tahminini yayınladı. Detaylar için Alfonso AI tahmin sayfasına göz atın."
    link = f"/ai/alfonso/{alfonso_slug}"
    yayin_tarihi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect("data/ganyaniq.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS haberler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                baslik TEXT,
                ozet TEXT,
                tam_metin TEXT,
                kaynak TEXT,
                yayin_tarihi TEXT,
                kategori TEXT,
                manşet INTEGER DEFAULT 0,
                ai_etiket TEXT,
                haber_link TEXT
            )
        ''')

        cursor.execute('''
            INSERT INTO haberler (baslik, ozet, tam_metin, kaynak, yayin_tarihi, kategori, manşet, ai_etiket, haber_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            baslik,
            ozet,
            "",
            "Alfonso AI",
            yayin_tarihi,
            "AI-Tahmin",
            0,
            "alfonso",
            link
        ))

        conn.commit()
        print(f"✅ Alfonso tahmin haberi eklendi: {baslik}")

    except Exception as e:
        print(f"❌ Hata: Alfonso haberi eklenemedi: {e}")

    finally:
        conn.close()


# Örnek kullanım:
# alfonso_tahmin_haberi_olustur("KOSU_582", "2025-06-02", "İzmir 5. Koşu", "izmir-5-kosu-2025-06-02")
