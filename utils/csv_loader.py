# ganyaniq_race_module/utils/csv_loader.py

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def load_csv_to_db(csv_folder):
    engine = create_engine(DATABASE_URL)
    for file in os.listdir(csv_folder):
        if file.endswith(".csv"):
            file_path = os.path.join(csv_folder, file)
            df = pd.read_csv(file_path)
            try:
                df.to_sql('race_results', con=engine, if_exists='append', index=False)
                print(f"Başarıyla yüklendi: {file}")
            except Exception as e:
                print(f"Yüklenirken hata: {file} -> {e}")
