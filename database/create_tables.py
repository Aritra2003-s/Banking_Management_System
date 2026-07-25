import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("database/banking.db")
cursor = conn.cursor()

# Enable Foreign Key Support
cursor.execute("PRAGMA foreign_keys = ON;")

# ==========================
# Admin Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'Admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ==========================
# Customer Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    address TEXT,
    date_of_birth DATE,
    aadhaar TEXT UNIQUE,
    pan TEXT UNIQUE,
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ==========================
# Account Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Account (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    account_number TEXT UNIQUE NOT NULL,
    account_type TEXT NOT NULL,
    balance REAL DEFAULT 0,
    pin TEXT NOT NULL,
    status TEXT DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(customer_id)
        REFERENCES Customer(customer_id)
        ON DELETE CASCADE
)
""")

# ==========================
# Transactions Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    balance_after REAL NOT NULL,
    receiver_account TEXT,
    description TEXT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(account_id)
        REFERENCES Account(account_id)
        ON DELETE CASCADE
)
""")

# ==========================
# Notification Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Notification (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(customer_id)
        REFERENCES Customer(customer_id)
        ON DELETE CASCADE
)
""")

# ==========================
# Password Reset Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS PasswordReset (
    reset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    reset_token TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    used INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id)
        REFERENCES Customer(customer_id)
        ON DELETE CASCADE

)
""")

# ==========================
# Audit Log Table
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS AuditLog (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_type TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    ip_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
               
               
""")



# Save changes
conn.commit()

print("=" * 50)
print("✅ Banking Database Created Successfully!")
print("Tables Created:")
print("1. Admin")
print("2. Customer")
print("3. Account")
print("4. Transactions")
print("5. Notification")
print("6. PasswordReset")
print("7. AuditLog")
print("=" * 50)

# Close connection
conn.close()