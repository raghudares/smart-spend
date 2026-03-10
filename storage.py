import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "smartspend.db"

class SQLiteStorage:

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                category TEXT,
                date TEXT,
                description TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                user_id INTEGER,
                category TEXT,
                amount REAL,
                PRIMARY KEY(user_id, category)
            )
        """)

        self.conn.commit()

    # ---------- AUTH ----------
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, self.hash_password(password))
            )
            self.conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Username already exists!")

    def login_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (username, self.hash_password(password))
        )
        result = cursor.fetchone()
        return result[0] if result else None

    # ---------- EXPENSES ----------
    def add_expense(self, user_id, amount, category, description):
        date = datetime.now().strftime("%Y-%m-%d")
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, amount, category, date, description)
        )
        self.conn.commit()

    def get_all_expenses(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, amount, category, date, description FROM expenses WHERE user_id=?",
            (user_id,)
        )
        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "amount": row[1],
                "category": row[2],
                "date": row[3],
                "description": row[4]
            }
            for row in rows
        ]

    # ---------- BUDGET ----------
    def set_budget(self, user_id, category, amount):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO budgets (user_id, category, amount) VALUES (?, ?, ?)",
            (user_id, category, amount)
        )
        self.conn.commit()

    def get_budgets(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT category, amount FROM budgets WHERE user_id=?",
            (user_id,)
        )
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}
