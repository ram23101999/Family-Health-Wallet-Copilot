import os
import mysql.connector
from mysql.connector import Error

def _connect():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "family_health_wallet")
    )

def db_status():
    try:
        conn = _connect()
        if conn.is_connected():
            conn.close()
            return True
    except Exception:
        return False
    return False

def init_db():
    if not db_status():
        return
    try:
        conn = _connect()
        cursor = conn.cursor()
        
        # Family Members Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS family_members (
                member_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100),
                relation VARCHAR(50),
                age INT,
                health_card_status VARCHAR(20),
                wallet_balance DECIMAL(10,2)
            )
        ''')
        
        # Transactions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallet_transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                member_id VARCHAR(50),
                txn_type VARCHAR(20),
                amount DECIMAL(10,2),
                description VARCHAR(255),
                txn_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database Init Error: {e}")

def save_transaction(member_id, txn_type, amount, description):
    if not db_status():
        return False
    try:
        conn = _connect()
        cursor = conn.cursor()
        query = "INSERT INTO wallet_transactions (member_id, txn_type, amount, description) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (member_id, txn_type, amount, description))
        
        # Update Balance
        if txn_type == "Recharge":
            cursor.execute("UPDATE family_members SET wallet_balance = wallet_balance + %s WHERE member_id = %s", (amount, member_id))
        elif txn_type == "Expense":
            cursor.execute("UPDATE family_members SET wallet_balance = wallet_balance - %s WHERE member_id = %s", (amount, member_id))
            
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error saving transaction: {e}")
        return False
