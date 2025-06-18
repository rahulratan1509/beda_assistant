# modules/memory_manager.py

import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join("data", "beda_memory.db")

# Ensure database and table exist
def init_memory_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fact TEXT NOT NULL,
        context TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# Save any user/assistant message
def save_to_memory(role, content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO memory (role, content, timestamp) VALUES (?, ?, ?)",
        (role, content, timestamp)
    )

    conn.commit()
    conn.close()

# Fetch recent messages
def fetch_recent_memory(limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM memory ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]  # Return in chronological order

# Save a persistent fact
def save_fact(fact, context=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO facts (fact, context, timestamp) VALUES (?, ?, ?)",
        (fact, context, timestamp)
    )

    conn.commit()
    conn.close()

# Load all saved facts
def load_all_facts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT fact FROM facts ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

# Initialize DB on import
init_memory_db()
