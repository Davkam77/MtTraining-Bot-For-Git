import sqlite3, os
from datetime import datetime

DB_PATH = "data/progress.db"
os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS weight (
    user_id INTEGER,
    weight REAL,
    date TEXT
)''')
conn.commit()

def save_weight(user_id: int, weight: float):
    c.execute("INSERT INTO weight VALUES (?, ?, ?)", (user_id, weight, datetime.now().isoformat()))
    conn.commit()

def get_weights(user_id: int):
    c.execute("SELECT weight, date FROM weight WHERE user_id = ?", (user_id,))
    return c.fetchall()