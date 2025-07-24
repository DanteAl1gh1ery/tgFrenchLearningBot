import sqlite3
import logging

#connect woth database
def create_connection (db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.info("Успішно підключено до БД: {db_file}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Помилка підключення до БД: {e}")
        return None
    
def create_table(conn):
    """Створює таблицю Users, якщо вона ще не існує."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                language_learning TEXT DEFAULT 'en'
            )
        """)
        conn.commit()
        logging.info("Таблицю Users створено (або вже існувала).")
    except sqlite3.Error as e:
        logging.error(f"Помилка створення таблиці Users: {e}")

def user_exists(conn, user_id):
    """Перевіряє, чи існує користувач з даним user_id."""
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        return cur.fetchone() is not None
    except sqlite3.Error as e:
        logging.error(f"Помилка перевірки існування користувача: {e}")
        return False

def create_user(conn, user_id, username):
    """Додає нового користувача в базу даних."""
    try:
        sql = ''' INSERT INTO Users(user_id,username)
                  VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (user_id, username))
        conn.commit()
        logging.info(f"Користувача з user_id {user_id} створено.")
        return cur.lastrowid
    except sqlite3.Error as e:
        logging.error(f"Помилка створення користувача: {e}")
        return None