@echo off
echo 📦 Flask kuruluyor...
pip install flask

echo 🧱 Veritabanı oluşturuluyor ve veriler yükleniyor...
python db\populate.py

echo ✅ Kurulum tamamlandı.
echo 🔁 Sunucuyu başlatmak için: python main.py
pause
