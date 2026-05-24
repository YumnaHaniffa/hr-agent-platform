#SQLite connection & Audit Log logic
import os
import sqlite3
from app.config import settings


def init_db():
    """
    Ensures the data directory exists and creates the 
    SQLite database tables if they do not exist.
    """
    # 1. Extract the folder path from your config (e.g., "data/")
    # settings.database_url is "data/hr_platform.db"
    db_path = settings.database_url
    db_dir = os.path.dirname(db_path)

    # 2. Create the data/ folder if it doesn't exist yet
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Created directory: {db_dir}")
    
    # 3. Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Initializing database tables...")

    # 4. Create the Long-Term Memory (LTM) Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ltm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. Create the Append-Only Audit Log Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT NOT NULL,
            node_name TEXT NOT NULL,
            state_data TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Save changes and close connection
    conn.commit()
    conn.close()
    print("Database initialization complete.")