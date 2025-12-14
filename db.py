import sqlite3

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
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(t_type, amount, interest, months, note):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transactions (type, amount, interest, months, note)
        VALUES (?, ?, ?, ?, ?)
    """, (t_type, amount, interest, months, note))
    conn.commit()
    conn.close()

def fetch_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")
    rows = cur.fetchall()
    conn.close()
    return rows
