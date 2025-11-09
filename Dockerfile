FROM python:3.11-slim

# 1) Uygulama dosyalarını kopyala
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 2) Çalışma klasörünü modülün içine al (önemli!)
WORKDIR /app/ganyaniq_race_module

# 3) Servisi başlat (app/main.py içindeki app nesnesi)
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
