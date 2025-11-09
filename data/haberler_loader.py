# haberler_loader.py (örnek)
import psycopg2
import os

def get_haber_by_id(haber_id):
    conn = psycopg2.connect(os.getenv("DB_URL"))
    cur = conn.cursor()
    cur.execute("SELECT id, baslik, icerik, kategori, resim_url FROM haberler WHERE id = %s", (haber_id,))
    haber = cur.fetchone()
    conn.close()
    return {
        "id": haber[0],
        "baslik": haber[1],
        "icerik": haber[2],
        "kategori": haber[3],
        "resim_url": haber[4]
    }

def update_haber(haber_id, baslik, icerik, kategori, resim_url):
    conn = psycopg2.connect(os.getenv("DB_URL"))
    cur = conn.cursor()
    cur.execute("UPDATE haberler SET baslik = %s, icerik = %s, kategori = %s, resim_url = %s WHERE id = %s",
                (baslik, icerik, kategori, resim_url, haber_id))
    conn.commit()
    conn.close()
