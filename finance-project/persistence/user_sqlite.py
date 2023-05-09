import sqlite3
import logging
from domain.user.persistence_interface import UserPersistenceInterface
from domain.user.user import User
from domain.user.factory import UserFactory

logging.basicConfig(
        filename="finance.log",
        level=logging.DEBUG,
        format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
    )


class UserPersistenceSqlite(UserPersistenceInterface):
    def get_all_users(self) -> list[User]:
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            # DONE homework try except return empty list if no db
            try:
                cursor.execute("SELECT * FROM users")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    logging.info(f"No users info found in database: " + str(e))
                    return []
            users_info = cursor.fetchall()
        factory = UserFactory()
        users = [factory.make_from_persistence(x) for x in users_info]
        return users

    def add(self, user: User):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    f"INSERT INTO users (id, username) VALUES ('{user.id}', '{user.username}')"
                )
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    logging.info(f"No users info found in database. Creating new table. " + str(e))
                    cursor.execute(
                        f"CREATE TABLE users (id TEXT PRIMARY KEY, username TEXT NOT NULL)"
                    )
                else:
                    logging.info("Could not create new table in database. Error: " + str(e))
                    raise e
                cursor.execute(
                    f"INSERT INTO users (id, username) VALUES ('{user.id}', '{user.username}')"
                )
            conn.commit()

    def delete(self, user_id: User.id):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"DELETE FROM users WHERE id='{user_id}'")
            except sqlite3.OperationalError as e:
                logging.error(f"Error: " + str(e))
                raise e
            conn.commit()

    def edit(self, user_id: User.id, username: str):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    f"UPDATE users SET (username)='{username}' WHERE id='{user_id}'"
                )
            except sqlite3.OperationalError as e:
                logging.error(f"Error: " + str(e))
                raise e
            conn.commit()
