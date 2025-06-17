import sqlite3
import os

DB_PATH = os.path.join("data", "database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn
