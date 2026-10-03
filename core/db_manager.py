# core/db_manager.py
import sqlite3
import hashlib
import os

DB_PATH = "cardscout.db"

def init_db():
    """Creates the necessary tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # User Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    ''')
    
    # Subscriptions Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            service_name TEXT NOT NULL,
            monthly_cost REAL NOT NULL,
            card_used TEXT NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')

    # Digital Wallet Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS wallet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            card_name TEXT NOT NULL,
            card_limit REAL NOT NULL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return pwd_hash, salt

def create_user(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        pwd_hash, salt = hash_password(password)
        c.execute("INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)", (username, pwd_hash, salt))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False 

def verify_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash, salt FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        stored_hash, salt = result
        pwd_hash, _ = hash_password(password, salt)
        return pwd_hash == stored_hash
    return False

# --- SUBSCRIPTION FUNCTIONS ---
def add_subscription(username, service_name, monthly_cost, card_used):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO subscriptions (username, service_name, monthly_cost, card_used) VALUES (?, ?, ?, ?)", 
              (username, service_name, monthly_cost, card_used))
    conn.commit()
    conn.close()

def get_subscriptions(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT service_name, monthly_cost, card_used FROM subscriptions WHERE username=?", (username,))
    results = c.fetchall()
    conn.close()
    return results

# --- NEW DIGITAL WALLET FUNCTIONS ---
def add_wallet_card(username, card_name, card_limit):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO wallet (username, card_name, card_limit) VALUES (?, ?, ?)", (username, card_name, card_limit))
    conn.commit()
    conn.close()

def remove_wallet_card(username, card_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM wallet WHERE username=? AND card_name=?", (username, card_name))
    conn.commit()
    conn.close()

def update_wallet_limit(username, card_name, new_limit):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE wallet SET card_limit=? WHERE username=? AND card_name=?", (new_limit, username, card_name))
    conn.commit()
    conn.close()

def get_wallet_cards(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT card_name, card_limit FROM wallet WHERE username=?", (username,))
    results = c.fetchall()
    conn.close()
    return results

# Initialize the database immediately
init_db()

def delete_subscription(username, service_name, card_used):
    """Deletes a tracked subscription linked to a SPECIFIC card."""
    conn = sqlite3.connect("cardscout.db")
    c = conn.cursor()
    c.execute("DELETE FROM subscriptions WHERE username = ? AND service_name = ? AND card_used = ?", (username, service_name, card_used))
    conn.commit()
    conn.close()

def update_subscription_card(username, service_name, new_card):
    """Re-routes an existing subscription to a different card."""
    conn = sqlite3.connect("cardscout.db")
    c = conn.cursor()
    c.execute("UPDATE subscriptions SET card_used = ? WHERE username = ? AND service_name = ?", (new_card, username, service_name))
    conn.commit()
    conn.close()