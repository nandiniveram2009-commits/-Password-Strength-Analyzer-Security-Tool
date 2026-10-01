import sqlite3
import os

DB_PATH = "data/analytics.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER,
            classification TEXT,
            password_length INTEGER,
            unique_ratio REAL,
            weakness_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def log_analysis(score: int, classification: str, length: int, unique_ratio: float, weakness_count: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analyses (score, classification, password_length, unique_ratio, weakness_count)
        VALUES (?, ?, ?, ?, ?)
    """, (score, classification, length, unique_ratio, weakness_count))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), AVG(score) FROM analyses")
    total, avg_score = cursor.fetchone()
    
    cursor.execute("SELECT classification, COUNT(*) FROM analyses GROUP BY classification")
    classifications = dict(cursor.fetchall())
    conn.close()
    
    return {
        "total_analyses": total or 0,
        "average_score": round(avg_score or 0.0, 2),
        "classifications": classifications
    }
