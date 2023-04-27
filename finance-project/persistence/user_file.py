import json
import logging
import uuid

from domain.user.factory import UserFactory
from domain.user.persistence_interface import UserPersistenceInterface
from domain.user.user import User

logging.basicConfig(
        filename="finance.log",
        level=logging.DEBUG,
        format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
    )


class FailedToWriteInPersistence(Exception):
    pass


class UserPersistenceFile(UserPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def get_all(self) -> list[User]:
        try:
            # DONE refactor with
            with open(self.__file_path) as file:
                contents = file.read()
                users_info = json.loads(contents)
                factory = UserFactory()
            return [factory.make_from_persistence(x) for x in users_info]
        except FailedToWriteInPersistence as e:
            # DONE homework, log error
            logging.error("Could not read file, reason: " + str(e))
            return []

    def add(self, user: User):
        current_users = self.get_all()
        current_users.append(user)
        users_info = [(str(u.id), u.username, u.stocks) for u in current_users]
        users_json = json.dumps(users_info)
        # DONE homework refactor with
        try:
            with open(self.__file_path, "w") as file:
                file.write(users_json)
        except FailedToWriteInPersistence as e:
            logging.error("Could not write user info to persistence. Error: " + str(e))
            raise e

    def delete(self, user_id: User.id):
        current_users = self.get_all()
        updated_users_list = [u for u in current_users if u.id != uuid.UUID(hex=user_id)]
        users_info = [(str(u.id), u.username, u.stocks) for u in updated_users_list]
        users_json = json.dumps(users_info)
        try:
            with open(self.__file_path, "w") as file:
                file.write(users_json)
        except FailedToWriteInPersistence as e:
            logging.error("Could not write user info to persistence. Error: " + str(e))
            raise e

    def edit(self, user_id: User.id, username: str):
        current_users = self.get_all()
        for user in current_users:
            if user.id == uuid.UUID(hex=user_id):
                user.username = username
            users_info = [(str(u.id), u.username, u.stocks) for u in current_users]
            users_json = json.dumps(users_info)
            try:
                with open(self.__file_path, "w") as f:
                    f.write(users_json)
            except FailedToWriteInPersistence as e:
                logging.error("Could not write user info to persistence. Error: " + str(e))
                raise e
