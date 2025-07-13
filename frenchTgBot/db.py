import sqlite3;

conn = sqlite3.connect("words.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        word TEXT,
        translation TEXT,
        transcription TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        correct_count INTEGER DEFAULT 0,
        incorrect_count INTEGER DEFAULT 0
    )
""")

conn.commit()