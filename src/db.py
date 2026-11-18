import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'prices.db')

def init_db():
    """Создаёт таблицу, если её ещё нет."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            marketplace TEXT NOT NULL,
            article TEXT,
            name TEXT,
            brand TEXT,
            price REAL,
            basic_price REAL,
            sizes_json TEXT,
            sizes_count INTEGER,
            supplier TEXT,
            rating REAL,
            feedbacks INTEGER,
            url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_to_sqlite(df, marketplace):
    """Сохраняет DataFrame в SQLite, добавляя timestamp."""
    init_db()
    df = df.copy()
    df['timestamp'] = datetime.now().isoformat()
    df['marketplace'] = marketplace

    columns = ['timestamp', 'marketplace', 'article', 'name', 'brand',
               'price', 'basic_price', 'sizes_json', 'sizes_count',
               'supplier', 'rating', 'feedbacks', 'url']
    df = df[[c for c in columns if c in df.columns]]

    conn = sqlite3.connect(DB_PATH)
    df.to_sql('prices', conn, if_exists='append', index=False)
    conn.close()
    print(f"Сохранено {len(df)} строк в {DB_PATH}")

def load_from_sqlite(marketplace=None):
    """Читает данные из SQLite (для анализа)."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM prices"
    if marketplace:
        query += f" WHERE marketplace = '{marketplace}'"
    df = pd.read_sql(query, conn)
    conn.close()
    return df