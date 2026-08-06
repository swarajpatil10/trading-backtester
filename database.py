import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    database_url=os.environ.get("DATABASE_URL")

    if database_url:
        conn = psycopg2.connect(database_url)
    else:
        conn = psycopg2.connect(
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
        )    
    return conn        
if __name__ == "__main__":
    conn = get_connection()
    print("Connected successfully:", conn)
    conn.close()