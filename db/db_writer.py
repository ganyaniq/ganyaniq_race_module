import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch

class DBWriter:
    def __init__(self, db_params):
        self.db_params = db_params
        self.conn = psycopg2.connect(**db_params)
        self.cur = self.conn.cursor()

    def save_records(self, table_name, records):
        if not records:
            return
        try:
            columns = records[0].keys()
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) ON CONFLICT DO NOTHING").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(columns))
            )
            values = [[record[col] for col in columns] for record in records]
            execute_batch(self.cur, query.as_string(self.conn), values)
            self.conn.commit()
        except Exception as e:
            print(f"Error saving records to DB: {e}")

    def close(self):
        self.cur.close()
        self.conn.close()
