import sqlite3
import os

DB_PATH = "data/memory.db"
os.makedirs("data", exist_ok=True)

def init_memory_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Memory DB initialized.")

if __name__ == "__main__":
    init_memory_db()
