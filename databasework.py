import sqlite3
from Accounts import Account

def get_account_list():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, [full name], Balance, [Account number], Condition, [Opening date], [National number], [Phone number] FROM Accounts")
    rows = cursor.fetchall()
    conn.close()
    return [Account(*row) for row in rows]

def search_account(search_term):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, [full name], Balance, [Account number], Condition, [Opening date], [National number], [Phone number]
        FROM Accounts
        WHERE [full name] LIKE ?
           OR [Account number] LIKE ? 
           OR [National number] LIKE ?
           OR [Phone number] LIKE ?
    """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    rows = cursor.fetchall()
    conn.close()
    return [Account(*row) for row in rows]

def create_account(full_name, balance, account_number, condition, opening_date, national_number, phone_number):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Accounts ([full name], Balance, [Account number], Condition, [Opening date], [National number], [Phone number])
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (full_name, balance, account_number, condition, opening_date, national_number, phone_number))
    conn.commit()
    conn.close()

def update_account(account_id, full_name, balance, account_number, condition, opening_date, national_number, phone_number):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Accounts
        SET [full name]=?, Balance=?, [Account number]=?, Condition=?, [Opening date]=?, [National number]=?, [Phone number]=?
        WHERE id=?
    """, (full_name, balance, account_number, condition, opening_date, national_number, phone_number, account_id))
    conn.commit()
    conn.close()

def delete_account(account_id):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Accounts WHERE id=?", (account_id,))
    conn.commit()
    conn.close()
