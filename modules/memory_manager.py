# modules/memory_manager.py

import sqlite3
from datetime import datetime

DB_PATH = "data/beda_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            emotion TEXT,
            topic TEXT,
            flag TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT NOT NULL,
            context TEXT,
            confidence REAL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_to_memory(role, content, emotion=None, topic=None, flag=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO memory (role, content, emotion, topic, flag, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (role, content, emotion, topic, flag, timestamp))
    conn.commit()
    conn.close()

def save_fact(fact, context=None, confidence=1.0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO facts (fact, context, confidence, timestamp)
        VALUES (?, ?, ?, ?)
    """, (fact, context, confidence, timestamp))
    conn.commit()
    conn.close()
    
def load_all_facts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT fact FROM facts ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def fetch_recent_memory(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, content, emotion, topic, flag, timestamp
        FROM memory ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]

# At bottom of your existing memory_manager.py
def fetch_facts(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT fact, context, timestamp FROM facts ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]

def clear_memory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memory")
    cursor.execute("DELETE FROM facts")
    conn.commit()
    conn.close()
