import sqlite3
from datetime import datetime

DB_PATH = "data/users.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()

        # Таблица профиля
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            user_id INTEGER PRIMARY KEY,
            weight REAL,
            goal REAL,
            height INTEGER,
            age INTEGER,
            gender TEXT,
            activity REAL
        )
        """)

        # Таблица истории веса
        cur.execute("""
        CREATE TABLE IF NOT EXISTS weight_history (
            user_id INTEGER,
            date TEXT,
            weight REAL
        )
        """)

        conn.commit()

def save_user_profile(user_id, weight, goal, height, age, gender, activity):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO user_profile (user_id, weight, goal, height, age, gender, activity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                weight=excluded.weight,
                goal=excluded.goal,
                height=excluded.height,
                age=excluded.age,
                gender=excluded.gender,
                activity=excluded.activity
        """, (user_id, weight, goal, height, age, gender, activity))
        conn.commit()

def add_weight_entry(user_id, weight):
    with get_connection() as conn:
        cur = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cur.execute("""
            INSERT INTO weight_history (user_id, date, weight)
            VALUES (?, ?, ?)
        """, (user_id, today, weight))
        conn.commit()

def get_user_profile(user_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT weight, goal, height, age, gender, activity
            FROM user_profile
            WHERE user_id = ?
        """, (user_id,))
        row = cur.fetchone()

    if row:
        return {
            "weight": row[0],
            "goal": row[1],
            "height": row[2],
            "age": row[3],
            "gender": row[4],
            "activity": row[5]
        }
    else:
        return None

def get_user_dashboard(user_id):
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM weight_logs WHERE user_id = ?", (user_id,))
        total_entries = cur.fetchone()[0]

        cur.execute("SELECT weight, timestamp FROM weight_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", (user_id,))
        last_entry = cur.fetchone()

        cur.execute("SELECT weight FROM weight_logs WHERE user_id = ? ORDER BY timestamp ASC LIMIT 1", (user_id,))
        first_weight = cur.fetchone()

    return {
        "total_entries": total_entries,
        "last_weight": last_entry[0] if last_entry else None,
        "last_date": last_entry[1] if last_entry else None,
        "first_weight": first_weight[0] if first_weight else None
    }

def update_steps(user_id: int, steps: int):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS steps (
                user_id INTEGER,
                date TEXT,
                steps INTEGER,
                PRIMARY KEY (user_id, date)
            )
        """)
        today = datetime.now().strftime("%Y-%m-%d")
        cur.execute("""
            INSERT INTO steps (user_id, date, steps)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, date) DO UPDATE SET
                steps = excluded.steps
        """, (user_id, today, steps))
        conn.commit()

def get_steps_by_user(user_id: int) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT SUM(steps) FROM steps WHERE user_id = ?
        """, (user_id,))
        result = cur.fetchone()[0]
        return result or 0
