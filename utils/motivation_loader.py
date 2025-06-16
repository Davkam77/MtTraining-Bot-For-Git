import json
import random

with open("data/motivations.json", "r", encoding="utf-8") as f:
    MOTIVATIONS = json.load(f)

def get_daily_motivation():
    return random.choice(MOTIVATIONS)
