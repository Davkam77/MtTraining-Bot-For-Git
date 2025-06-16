import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io
import sqlite3
from utils.database import get_connection

def generate_chart_human(user_id):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT date, weight FROM weight_history
            WHERE user_id = ?
            ORDER BY date ASC
        """, (user_id,))
        rows = cur.fetchall()

    if not rows or len(rows) < 2:
        return None

    # Преобразуем строки в datetime
    dates = [datetime.strptime(row[0], "%Y-%m-%d") for row in rows]
    weights = [row[1] for row in rows]

    # Расчёт тренда
    diff = weights[-1] - weights[0]
    days = (dates[-1] - dates[0]).days
    sign = "минус" if diff < 0 else "плюс"
    trend_text = f"📆 За {days} дн.: {sign} {abs(diff):.1f} кг"

    # Построение графика
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(dates, weights, marker="o", linewidth=2)
    ax.set_title("📉 Динамика веса")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Вес (кг)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.grid(True)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf, trend_text
