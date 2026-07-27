import sqlite3

DATABASE = "database/banking.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Alias for backward compatibility
def get_connection():
    return get_db_connection()