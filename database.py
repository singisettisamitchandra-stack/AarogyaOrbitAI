
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "aarogyaorbit.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS grocery_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                budget REAL NOT NULL,
                days INTEGER NOT NULL,
                preferences TEXT,
                plan TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_chat(user_message: str, ai_response: str):
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO chat_history (user_message, ai_response) VALUES (?, ?)",
            (user_message, ai_response),
        )


def get_chat_history(limit: int = 20):
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM chat_history ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def save_grocery_plan(
    budget: float,
    days: int,
    preferences: str,
    plan: str,
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO grocery_plans (budget, days, preferences, plan)
            VALUES (?, ?, ?, ?)
            """,
            (budget, days, preferences, plan),
        )
