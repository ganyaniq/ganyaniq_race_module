import psycopg2
from psycopg2 import sql

class URLManager:
    def __init__(self, db_params):
        self.conn = psycopg2.connect(**db_params)
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS url_list (
                    id SERIAL PRIMARY KEY,
                    url TEXT UNIQUE NOT NULL,
                    category TEXT,
                    last_fetched TIMESTAMP
                )
            """)
            self.conn.commit()

    def add_url(self, url, category):
        with self.conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO url_list (url, category) VALUES (%s, %s)
                    ON CONFLICT (url) DO NOTHING
                """, (url, category))
                self.conn.commit()
            except Exception as e:
                print(f"Error adding URL: {e}")

    def get_pending_urls(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT url FROM url_list WHERE last_fetched IS NULL OR last_fetched < NOW() - INTERVAL '1 hour'
            """)
            return [row[0] for row in cur.fetchall()]

    def update_fetched_time(self, url):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE url_list SET last_fetched = NOW() WHERE url = %s
            """, (url,))
            self.conn.commit()

    def close(self):
        self.conn.close()
