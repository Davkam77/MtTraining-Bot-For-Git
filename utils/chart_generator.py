import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io
import os
import json


def generate_chart_human(user_id):
    # Пример: загрузка данных из файла data/weight_data.json
    data_file = f"data/weight_{user_id}.json"
    if not os.path.exists(data_file):
        return None

    with open(data_file, "r") as f:
        weight_data = json.load(f)  # [("2025-06-10", 98), ...]

    if not weight_data or len(weight_data) < 2:
        return None

    dates = [datetime.strptime(d, "%Y-%m-%d") for d, _ in weight_data]
    weights = [w for _, w in weight_data]

    diff = weights[-1] - weights[0]
    days = (dates[-1] - dates[0]).days
    sign = "минус" if diff < 0 else "плюс"
    trend_text = f"📆 {days} дней: {sign} {abs(diff):.1f} кг"

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(dates, weights, marker="o", linewidth=2)
    ax.set_title("Динамика веса")
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
