#!/bin/bash

echo "📦 Flask kuruluyor..."
pip install flask

echo "🧱 Veritabanı oluşturuluyor ve veriler yükleniyor..."
python3 db/populate.py

echo "✅ Kurulum tamamlandı."
echo "🔁 Sunucuyu başlatmak için: python3 main.py"
