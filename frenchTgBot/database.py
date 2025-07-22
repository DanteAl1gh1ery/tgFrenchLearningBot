# database.py
import sqlite3

DB_NAME = "words.db"

def init_db():
    """Ініціалізує базу даних, створює таблицю, якщо вона не існує."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # SQL-запит для створення таблиці з УСІМА потрібними колонками
    # IF NOT EXISTS - дуже важлива частина, вона запобігає помилці, якщо таблиця вже є
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        word TEXT NOT NULL,
        translation TEXT NOT NULL,
        transcription TEXT,
        user_word_number INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        correct_count INTEGER DEFAULT 0,
        incorrect_count INTEGER DEFAULT 0
    );
    """)
    
    conn.commit()
    conn.close()
    print("Базу даних ініціалізовано.")

def add_word(user_id: int, word: str, translation: str, transcription: str) -> int:
    """
    Додає нове слово в базу даних і повертає його порядковий номер для користувача.
    """
    conn = None  # Ініціалізуємо conn
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # 1. Рахуємо, скільки слів вже є у цього користувача
        cursor.execute("SELECT COUNT(id) FROM words WHERE user_id = ?", (user_id,))
        # fetchone() поверне кортеж, наприклад (5,), тому беремо перший елемент [0]
        count = cursor.fetchone()[0]
        
        # 2. Новий порядковий номер = поточна кількість + 1
        new_word_number = count + 1

        # 3. Додаємо слово в базу разом з його новим номером
        cursor.execute(
            "INSERT INTO words (user_id, word, translation, transcription, user_word_number) VALUES (?, ?, ?, ?, ?)",
            (user_id, word, translation, transcription, new_word_number)
        )
        conn.commit()
        
        # 4. Повертаємо номер, щоб показати його користувачеві
        return new_word_number

    except sqlite3.Error as e:
        print(f"Помилка при додаванні слова: {e}")
        return 0 # Повертаємо 0 у випадку помилки
    finally:
        if conn:
            conn.close()