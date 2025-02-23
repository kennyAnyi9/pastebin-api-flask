# database.py
import os
import psycopg2
from psycopg2 import pool
from nanoid import generate

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Database connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # min and max connections
    dsn=DATABASE_URL
)

def create_paste(content):
    conn = db_pool.getconn()
    try:
        paste_id = generate_unique_id()
        query = """
            INSERT INTO pastes (paste_id, content)
            VALUES (%s, %s)
            RETURNING paste_id;
        """
        with conn.cursor() as cur:
            cur.execute(query, (paste_id, content))
            conn.commit()
            return paste_id
    finally:
        db_pool.putconn(conn)

def get_paste(paste_id):
    conn = db_pool.getconn()
    try:
        query = """
            SELECT content
            FROM pastes
            WHERE paste_id = %s;
        """
        with conn.cursor() as cur:
            cur.execute(query, (paste_id,))
            result = cur.fetchone()
            return result[0] if result else None
    finally:
        db_pool.putconn(conn)

def generate_unique_id():
    return generate(size=6)  # Generates a 6-character unique ID