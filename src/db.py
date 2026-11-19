import sqlite3
import pandas as pd
import datetime as dt
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'prices.db')

def init_db():
    """Создаёт таблицу, если её ещё нет."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            article TEXT,
            name TEXT,
            brand TEXT,
            colors_json TEXT,
            price REAL,
            basic_price REAL,
            sizes_json TEXT,
            sizes_count INTEGER,
            supplier TEXT,
            rating REAL,
            feedbacks INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_to_sqlite(df):
    """Сохраняет DataFrame в SQLite, добавляя date."""
    init_db()
    df = df.copy()
    df['date'] = dt.date.today().isoformat()

    columns = ['date', 'article', 'name', 'brand', 
               'colors_json', 'price', 'basic_price', 'sizes_json', 
               'sizes_count', 'supplier', 'rating', 'feedbacks']
    df = df[[c for c in columns if c in df.columns]]

    conn = sqlite3.connect(DB_PATH)
    df.to_sql('prices', conn, if_exists='append', index=False)
    conn.close()
    print(f"Сохранено {len(df)} строк в {DB_PATH}")

def load_from_sqlite():
    """Читает данные из SQLite (для анализа)."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM prices"
    df = pd.read_sql(query, conn)
    conn.close()
    return df