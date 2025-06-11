import sqlite3
from datetime import datetime

# Connect to (or create) the memory database
conn = sqlite3.connect("beda_memory.db")  # use "/mnt/data/beda_memory.db" if you're working inside a special runtime
cursor = conn.cursor()

# Create a table for long-term memory
cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,           -- 'user' or 'assistant'
    content TEXT NOT NULL,        -- actual message content
    emotion TEXT,                 -- optional emotion tag (happy, sad, neutral, etc.)
    topic TEXT,                   -- optional topic tag (tech, life, etc.)
    flag TEXT,                    -- optional user-defined flag (important, question, etc.)
    timestamp TEXT NOT NULL       -- ISO format datetime
)
""")

# Commit changes and close setup connection
conn.commit()
conn.close()

print("✅ SQLite memory schema created successfully.")
