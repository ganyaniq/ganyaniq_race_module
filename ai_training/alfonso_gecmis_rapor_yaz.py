# 📁 MODÜL: alfonso_gecmis_rapor_yaz.py
# 🧾 AÇIKLAMA: Alfonso'nun geçmiş tahminlerini sonuçlarla eşleştirir, detaylı haber üretir

import sqlite3
from datetime import datetime, timedelta


def alfonso_dun_raporu_olustur():
    tarih = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    yayin_tarihi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    baslik = f"Alfonso’nun Dünkü Başarıları – {tarih}"
    kategori = "AI-Rapor"
    kaynak = "Alfonso AI"
    ai_etiket = "alfonso_gecmis"

    try:
        conn = sqlite3.connect("data/ganyaniq.db")
        cursor = conn.cursor()

        # Gecmis tahmin ve sonuclari cek
        cursor.execute("""
            SELECT t.kosu_id, t.at_adi AS tahmin, s.kazanan_at, 
                   CASE WHEN t.at_adi = s.kazanan_at THEN '✅ Evet' ELSE '❌ Hayır' END AS isabet
            FROM tahminler t
            JOIN yaris_sonuclari s ON t.kosu_id = s.kosu_id
            WHERE t.tarih = ?
        """, (tarih,))

        satirlar = cursor.fetchall()

        if not satirlar:
            print("❌ Hiç eşleşen veri bulunamadı.")
            return

        # Detay metin oluştur
        tam_metin = f"<h3>📅 Alfonso’nun Tahmin Raporu – {tarih}</h3>"
        tam_metin += "<table border='1'><tr><th>Koşu</th><th>Tahmin</th><th>Kazanan</th><th>Başarı</th></tr>"

        for row in satirlar:
            kosu_id, tahmin, kazanan, isabet = row
            tam_metin += f"<tr><td>{kosu_id}</td><td>{tahmin}</td><td>{kazanan}</td><td>{isabet}</td></tr>"

        tam_metin += "</table><br>"
        tam_metin += "<p>🔮 <a href='/ai/alfonso/bugun'>Alfonso'nun Bugünkü Tahminlerini Gör</a></p>"

        # Haber olarak ekle
        cursor.execute("""
            INSERT INTO haberler (baslik, ozet, tam_metin, kaynak, yayin_tarihi, kategori, manşet, ai_etiket, haber_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            baslik,
            "Alfonso’nun dünkü tahminlerine ait başarı analizi yayınlandı.",
            tam_metin,
            kaynak,
            yayin_tarihi,
            kategori,
            1,
            ai_etiket,
            None
        ))

        conn.commit()
        print(f"✅ Alfonso geçmiş tahmin haberi eklendi: {baslik}")

    except Exception as e:
        print(f"❌ Hata: Geçmiş tahmin haberi eklenemedi: {e}")

    finally:
        conn.close()


# Örnek tetikleme:
# alfonso_dun_raporu_olustur()
