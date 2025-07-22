# database.py
import sqlite3

DB_NAME = "words.db"

def add_word(user_id: int, word: str, translation: str, transcription: str):
    """Додає нове слово в базу даних."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO words (user_id, word, translation, transcription) VALUES (?, ?, ?, ?)",
            (user_id, word, translation, transcription)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Помилка при додаванні слова: {e}")
    finally:
        if conn:
            conn.close()

# Тут можна додати інші функції: get_words, delete_word і т.д.