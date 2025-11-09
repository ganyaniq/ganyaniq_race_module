
## 🔗 Erişim

- [localhost:5000/program](http://localhost:5000/program) → Yarış programı
- [localhost:5000/sonuclar](http://localhost:5000/sonuclar) → Yarış sonuçları

## 🗂 Dosya Yapısı

- `data/` → JSON ve CSV kaynak dosyaları
- `parser/` → Verileri ayrıştıran modüller
- `db/` → SQLite modelleri ve yükleyici
- `templates/` → HTML sayfa şablonları
- `main.py` → Flask uygulaması

## 📋 Açıklama

Veri yapıları:
- JSON: Her yarış ve atlar detaylı biçimde (`isim`, `jokey`, `handikap`…)
- CSV: Her sonucun detayları (`at`, `derece`, `ganyan`, `sıra`, `pist`…)

Tam entegrasyon ve görüntüleme sağlar. Simülasyon yok, gerçek veri kullanıma hazırdır.
