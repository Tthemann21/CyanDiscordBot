import sqlite3
from dataclasses import dataclass
from typing import Self

DB_FILE = "db_discordbot.db"


@dataclass
class PlayerUser:
    """Dataclass representing a player in the database."""

    user_id: int
    balance: int
    level: int
    xp: int

    @classmethod
    def default(cls, user_id: int) -> Self:
        """Create a user with default starting values."""
        return cls(user_id=user_id, balance=500, level=1, xp=0)


class PlayerDatabase:
    """Database manager for player currency and progression data"""

    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self.con = sqlite3.connect(self.db_file, check_same_thread=False)
        self.setup()

    def setup(self) -> None:
        try:
            cursor = self.con.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS player_currency (
                    user_id INTEGER PRIMARY KEY,
                    balance INTEGER,
                    xp INTEGER,
                    level INTEGER
                )
            """)
            self.con.commit()
            print("Database setup completed.")
        except sqlite3.Error as e:
            print(f"ERROR: Could not set up database: {e}")

    def fetch_user(self, user_id: int) -> PlayerUser:
        try:
            cursor = self.con.cursor()
            cursor.execute(
                "SELECT user_id, balance, level, xp FROM player_currency WHERE user_id = ?",
                (user_id,),
            )
            result = cursor.fetchone()

            if result is None:
                # may have to be refactored into execute many depending on popularity
                # Create new user with default values
                new_user = PlayerUser.default(user_id)
                cursor.execute(
                    "INSERT INTO player_currency (user_id, balance, level, xp) VALUES (?, ?, ?, ?)",
                    (new_user.user_id, new_user.balance, new_user.level, new_user.xp),
                )
                self.con.commit()
                return new_user
            else:
                return PlayerUser(*result)
        except sqlite3.Error as e:
            try:
                self.con.rollback()
            except Exception:
                pass
            print(f"Database error during fetch: {e}")
            return PlayerUser.default(user_id)

    def fetch_users(self, user_ids: list[int]) -> list[PlayerUser]:
        if not user_ids:
            return []

        try:
            cursor = self.con.cursor()
            placeholders = ", ".join("?" * len(user_ids))
            cursor.execute(
                f"SELECT user_id, balance, level, xp FROM player_currency WHERE user_id IN ({placeholders})",
                user_ids,
            )
            results = [
                PlayerUser(uid, balance, level, xp)
                for (uid, balance, level, xp) in cursor.fetchall()
            ]

            # Find which users exist
            existing_ids = {u.user_id for u in results}
            missing_ids = set(user_ids) - existing_ids

            # Create missing users
            if missing_ids:
                new_users = [PlayerUser.default(uid) for uid in missing_ids]
                rows = [(u.user_id, u.balance, u.level, u.xp) for u in new_users]
                cursor.executemany(
                    "INSERT INTO player_currency (user_id, balance, level, xp) VALUES (?, ?, ?, ?)",
                    rows,
                )
                self.con.commit()
                results.extend(new_users)

            return results
        except sqlite3.Error as e:
            try:
                self.con.rollback()
            except Exception:
                pass
            print(f"Database error during fetch_users: {e}")
            return []

    def update_user(self, user: PlayerUser) -> bool:
        try:
            cursor = self.con.cursor()
            cursor.execute(
                "UPDATE player_currency SET balance = ?, level = ?, xp = ? WHERE user_id = ?",
                (user.balance, user.level, user.xp, user.user_id),
            )
            self.con.commit()
            return True
        except sqlite3.Error as e:
            try:
                self.con.rollback()
            except Exception:
                pass
            print(f"Database error during update: {e}")
            return False

    def close(self) -> None:
        """Close the underlying sqlite3 connection

        Safe to call multiple times
        """
        try:
            try:
                self.con.commit()
            except Exception:
                try:
                    self.con.rollback()
                except Exception:
                    pass
            try:
                self.con.close()
            except Exception:
                pass
        except Exception:
            pass
