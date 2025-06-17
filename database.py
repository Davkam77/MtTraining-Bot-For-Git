import sqlite3
import os

DB_PATH = os.path.join("data", "database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_motivation_table():
    db = get_db_connection()
    db.execute("""
        CREATE TABLE IF NOT EXISTS motivation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
