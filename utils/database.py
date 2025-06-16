import sqlite3
from datetime import datetime

DB_PATH = "data/users.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()

        # Профиль пользователя
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

        # История веса
        cur.execute("""
        CREATE TABLE IF NOT EXISTS weight_history (
            user_id INTEGER,
            date TEXT,
            weight REAL
        )
        """)

        # Логи веса
        cur.execute("""
        CREATE TABLE IF NOT EXISTS weight_logs (
            user_id INTEGER,
            weight REAL,
            timestamp TEXT
        )
        """)

        # План питания
        cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_mealplan (
            user_id INTEGER,
            date TEXT,
            meals TEXT
        )
        """)

        # Шаги
        cur.execute("""
        CREATE TABLE IF NOT EXISTS steps (
            user_id INTEGER,
            date TEXT,
            steps INTEGER,
            PRIMARY KEY (user_id, date)
        )
        """)

        # Настройки тренировок
        cur.execute("""
        CREATE TABLE IF NOT EXISTS workout_settings (
            user_id INTEGER PRIMARY KEY,
            duration_minutes INTEGER,
            months INTEGER,
            start_date TEXT
        )
        """)

        # Тренировки по дням
        cur.execute("""
        CREATE TABLE IF NOT EXISTS daily_workout (
            user_id INTEGER,
            date TEXT,
            workout TEXT,
            PRIMARY KEY (user_id, date)
        )
        """)

        conn.commit()

# ⬇️ Работа с профилем
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
    return None

def get_all_users():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM user_profile")
        return [row[0] for row in cur.fetchall()]

# ⬇️ Вес
def add_weight_entry(user_id, weight):
    with get_connection() as conn:
        cur = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().isoformat()

        cur.execute("""
            INSERT INTO weight_history (user_id, date, weight)
            VALUES (?, ?, ?)
        """, (user_id, today, weight))

        cur.execute("""
            INSERT INTO weight_logs (user_id, weight, timestamp)
            VALUES (?, ?, ?)
        """, (user_id, weight, timestamp))

        conn.commit()

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

# ⬇️ Шаги
def update_steps(user_id: int, steps: int):
    with get_connection() as conn:
        cur = conn.cursor()
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
        cur.execute("SELECT SUM(steps) FROM steps WHERE user_id = ?", (user_id,))
        result = cur.fetchone()[0]
        return result or 0

# ⬇️ План питания
def save_mealplan(user_id, date, meals_text):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO daily_mealplan (user_id, date, meals)
            VALUES (?, ?, ?)
        """, (user_id, date, meals_text))
        conn.commit()

def get_today_mealplan(user_id):
    with get_connection() as conn:
        cur = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cur.execute("""
            SELECT meals FROM daily_mealplan
            WHERE user_id = ? AND date = ?
        """, (user_id, today))
        row = cur.fetchone()
        return row[0] if row else None

# ⬇️ Тренировки
def save_workout_settings(user_id, duration_minutes, months):
    with get_connection() as conn:
        cur = conn.cursor()
        start_date = datetime.now().strftime("%Y-%m-%d")
        cur.execute("""
            INSERT INTO workout_settings (user_id, duration_minutes, months, start_date)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                duration_minutes = excluded.duration_minutes,
                months = excluded.months,
                start_date = excluded.start_date
        """, (user_id, duration_minutes, months, start_date))
        conn.commit()

def get_workout_settings(user_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT duration_minutes, months, start_date
            FROM workout_settings
            WHERE user_id = ?
        """, (user_id,))
        row = cur.fetchone()

    if row:
        return {
            "duration_minutes": row[0],
            "months": row[1],
            "start_date": row[2]
        }
    return None

def save_daily_workout(user_id, date, workout_text):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO daily_workout (user_id, date, workout)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, date) DO UPDATE SET
                workout = excluded.workout
        """, (user_id, date, workout_text))
        conn.commit()

def get_today_workout(user_id):
    with get_connection() as conn:
        cur = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        cur.execute("""
            SELECT workout FROM daily_workout
            WHERE user_id = ? AND date = ?
        """, (user_id, today))
        row = cur.fetchone()
        return row[0] if row else None
