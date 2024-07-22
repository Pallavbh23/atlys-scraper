import json
from pathlib import Path

DB_FILE = Path("data/scraped_products.json")

def load_db():
    if DB_FILE.exists():
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return []

def save_db(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)