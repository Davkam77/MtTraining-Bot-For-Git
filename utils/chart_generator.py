import matplotlib.pyplot as plt
from database.db import get_weights
from io import BytesIO

def generate_chart(user_id: int):
    data = get_weights(user_id)
    if not data:
        return None
    weights, dates = zip(*data)
    fig, ax = plt.subplots()
    ax.plot(dates, weights, marker='o')
    ax.set_title("Прогресс веса")
    ax.set_ylabel("Вес (кг)")
    ax.tick_params(axis='x', rotation=45)
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf