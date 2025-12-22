import sqlite3
from datetime import datetime

DB_NAME = "finance.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            amount REAL,
            interest REAL,
            months INTEGER,
            note TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(t_type, amount, interest, months, note):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transactions
        (type, amount, interest, months, note, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        t_type,
        amount,
        interest,
        months,
        note,
        datetime.now().strftime("%Y-%m-%d")
    ))
    conn.commit()
    conn.close()

def fetch_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_filtered(t_type, start_date, end_date, keyword):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM transactions
        WHERE type = ?
        AND created_at BETWEEN ? AND ?
        AND note LIKE ?
        ORDER BY created_at DESC
    """, (
        t_type,
        start_date,
        end_date,
        f"%{keyword}%"
    ))
    rows = cur.fetchall()
    conn.close()
    return rows
