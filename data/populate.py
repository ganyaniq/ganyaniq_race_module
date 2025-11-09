# ganyaniq_race_module/populate.py
from ganyaniq_race_module.db.models import create_tables
from ganyaniq_race_module.parser.parse_program import parse_program
from ganyaniq_race_module.parser.parse_results import parse_results
import sqlalchemy
import json
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://max_user:...@dpg-cvits1ali9vc73djuurg-a/yaris_veritabani")
engine = sqlalchemy.create_engine(DATABASE_URL)
conn = engine.connect()

# Veritabanını oluştur
create_tables(engine)

# Program verisini ekle
program = parse_program("ganyaniq_race_module/data/program_ornek.json")
for row in program:
    conn.execute(
        sqlalchemy.text("""
            INSERT INTO program (tarih, saat, kosu_no, kosu_adi, hipodrom, mesafe, pist, hava, atlar)
            VALUES (:tarih, :saat, :kosu_no, :kosu_adi, :hipodrom, :mesafe, :pist, :hava, :atlar)
        """),
        {
            **row,
            "atlar": json.dumps(row["atlar"])
        }
    )

# Sonuç verisini ekle
sonuclar = parse_results("ganyaniq_race_module/data/sonuclar_ornek.csv")
for row in sonuclar:
    conn.execute(
        sqlalchemy.text("""
            INSERT INTO sonuclar (tarih, kosu_no, kosu_adi, at_ismi, jokey, antrenor, ganyan, derece, sira, mesafe, pist)
            VALUES (:tarih, :kosu_no, :kosu_adi, :at_ismi, :jokey, :antrenor, :ganyan, :derece, :sira, :mesafe, :pist)
        """),
        row
    )

conn.commit()
conn.close()
