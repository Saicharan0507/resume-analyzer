import sqlite3
import json

DB_PATH = "candidates.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                score REAL,
                skills TEXT,
                status TEXT
            )
        ''')
        conn.commit()

init_db()

def save_candidate(data):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        skills_str = json.dumps(data.get('skills', []))
        cursor.execute(
            "INSERT INTO candidates (name, score, skills, status) VALUES (?, ?, ?, ?)", 
            (data.get('name'), data.get('score'), skills_str, data.get('status', 'Applied'))
        )
        conn.commit()

def get_candidates():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, score, skills, status FROM candidates ORDER BY score DESC")
        rows = cursor.fetchall()
        return [{"name": r[0], "score": r[1], "skills": json.loads(r[2]), "status": r[3]} for r in rows]

def update_status(name, status):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE candidates SET status = ? WHERE name = ?", (status, name))
        conn.commit()

def search_candidates(skill):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = f"%{skill}%"
        cursor.execute("SELECT name, score, skills, status FROM candidates WHERE skills LIKE ? ORDER BY score DESC", (query,))
        rows = cursor.fetchall()
        return [{"name": r[0], "score": r[1], "skills": json.loads(r[2]), "status": r[3]} for r in rows]
