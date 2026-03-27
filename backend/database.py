import sqlite3

DB_PATH = "candidates.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                score REAL
            )
        ''')
        conn.commit()

init_db()

def save_candidate(data):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO candidates (name, score) VALUES (?, ?)", (data['name'], data['score']))
        conn.commit()

def get_candidates():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, score FROM candidates ORDER BY score DESC")
        rows = cursor.fetchall()
        return [{"name": row[0], "score": row[1]} for row in rows]
