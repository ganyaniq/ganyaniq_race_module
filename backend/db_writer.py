import psycopg2
from psycopg2.extras import execute_values
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
}

class DBWriter:
    def __init__(self):
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()

    def insert_kategoriler(self, kategoriler: List[Dict]):
        query = """
        INSERT INTO kategoriler (id, name, slug, description)
        VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            slug = EXCLUDED.slug,
            description = EXCLUDED.description;
        """
        values = [(k['id'], k['name'], k['slug'], k['description']) for k in kategoriler]
        execute_values(self.cursor, query, values)
        self.conn.commit()

    def insert_alt_kategoriler(self, alt_kategori_slug: str, items: List[Dict]):
        query = """
        INSERT INTO alt_kategoriler (slug, name, description, kategori_slug)
        VALUES %s
        ON CONFLICT (slug) DO UPDATE SET
            name = EXCLUDED.name,
            description = EXCLUDED.description;
        """
        values = [(item['slug'], item['name'], item['description'], alt_kategori_slug) for item in items]
        execute_values(self.cursor, query, values)
        self.conn.commit()

    def insert_detay(self, slug: str, detay: Dict):
        query = """
        INSERT INTO detaylar (slug, name, description, gecmis_kosular, agf, son_sonuc)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (slug) DO UPDATE SET
            name = EXCLUDED.name,
            description = EXCLUDED.description,
            gecmis_kosular = EXCLUDED.gecmis_kosular,
            agf = EXCLUDED.agf,
            son_sonuc = EXCLUDED.son_sonuc;
        """
        self.cursor.execute(query, (
            slug,
            detay['name'],
            detay['description'],
            detay['gecmis_kosular'],
            detay['agf'],
            detay['son_sonuc']
        ))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
