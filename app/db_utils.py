import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="yaris_veritabani",
        user="max_user",
        password="r6P54e4ViGiYlVx7rkwLskmQhq830NN8Y",
        host="dpg-cvits1ali9vc73djuurg-a",
        port=5432
    )
