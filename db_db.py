import sqlite3
from typing import Optional

DB_FILE = "db_discordbot.db"
startingBalance = 500
startingLevel = 1
startingXp = 0

#----Database setup----#
def database_setup():
    try:
        with sqlite3.connect(DB_FILE) as con:
            cursor = con.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS player_currency (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER,
                xp INTEGER,
                level INTEGER
                        )
                """)
            con.commit()
            print("Database setup completed.")
    except sqlite3.Error as e:
        print(f"ERROR: Could not set up database: {e}")

#----Get or create user ----#
def get_or_create_user(user_id: int):
    try:
        with sqlite3.connect(DB_FILE) as con:
            cursor = con.cursor()

            cursor.execute('SELECT balance FROM player_currency WHERE user_id = ?', (user_id,))
            result: Optional[tuple] = cursor.fetchone()

            if result is None:
                #may have to be refactored into execute many depending on popularity
                # user does not exist insert new record in table
                cursor.execute(
                    'INSERT INTO player_currency (user_id, balance, level, xp) VALUES (?, ?, ?, ?)',
                    (user_id, startingBalance, startingLevel, startingXp)
                )
                con.commit()
                return startingBalance, startingLevel, startingXp
            else:
                #User exists return current balance
                return result[0]
    except sqlite3.Error as e:
        print(f"Database error during read/create: {e}")
        return 0


# bal = bal + change
#----Add to user balance----#
def add_balance(user_id: int, amount_change: int):
    try:
        with sqlite3.connect(DB_FILE) as con:
            cursor = con.cursor()

            cursor.execute('SELECT balance FROM player_currency WHERE user_id = ?', (user_id,))
            current_balance = cursor.fetchone()[0]

            if current_balance + amount_change < 0:
                return False

            cursor.execute(
                'UPDATE player_currency SET balance = balance + ? WHERE user_id = ?',
                (amount_change,user_id)
            )
            con.commit()
            return True
    except sqlite3.Error as e:
        print(f"Database error during update: {e}")
        return False

# bal = new_balance
#----Set user balance----#
def set_balance(user_id: int, new_balance: int):
    if new_balance < 0:
        return False
    try:
        with sqlite3.connect(DB_FILE) as con:
            cursor = con.cursor()

            cursor.execute(
                'UPDATE player_currency SET balance = ? WHERE user_id = ?',
                (new_balance,user_id)
            )
            con.commit()
            return True
    except sqlite3.Error as e:
        print(f"Database error during update: {e}")
        return False
    
#----Set user level----#
def set_level(user_id: int, new_level: int):
    if new_level < 0:
        return False
    try:    
        with sqlite3.connect(DB_FILE) as con:
            cursor = con.cursor()

            cursor.execute(
                'UPDATE player_currency SET level = ? WHERE user_id = ?',
                (new_level,user_id)
            )
            con.commit()
            return True
    except sqlite3.Error as e:
        print(f"Database error during update: {e}")
        return False

#----Add to user XP----#
def add_xp(user_id: int, xp_change: int):
    try:    
        with sqlite3.connect(DB_FILE) as con:
            cursor = con.cursor()

            cursor.execute('SELECT xp FROM player_currency WHERE user_id = ?', (user_id,))
            current_xp = cursor.fetchone()[0]

            if current_xp + xp_change < 0:
                return False
            
            cursor.execute(
                'UPDATE player_currency SET xp = xp + ? WHERE user_id = ?',
                (xp_change,user_id)
            )
            con.commit()
            return True
    except sqlite3.Error as e:
        print(f"Database error during update: {e}")
        return False

#----Set user XP----#
def set_xp(user_id: int, new_xp: int):
    if new_xp < 0:
        return False
    try:    
        with sqlite3.connect(DB_FILE) as con:
            cursor = con.cursor()

            cursor.execute(
                'UPDATE player_currency SET xp = ? WHERE user_id = ?',
                (new_xp,user_id)
            )
            con.commit()
            return True
    except sqlite3.Error as e:
        print(f"Database error during update: {e}")
        return False