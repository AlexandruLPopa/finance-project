import json
import logging
import uuid

from domain.user.factory import UserFactory
from domain.user.persistence_interface import UserPersistenceInterface
from domain.user.user import User


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
        except Exception as e:
            # DONE homework, log error
            logging.warning("Could not read file, reason: " + str(e))
            return []

    def add(self, user: User):
        current_users = self.get_all()
        current_users.append(user)
        users_info = [(str(u.id), u.username, u.stocks) for u in current_users]
        users_json = json.dumps(users_info)
        # DONE homework refactor with
        with open(self.__file_path, "w") as file:
            file.write(users_json)

    def delete(self, user_id: User.id):
        current_users = self.get_all()
        updated_users_list = [u for u in current_users if u.id != uuid.UUID(hex=user_id)]
        users_info = [(str(u.id), u.username, u.stocks) for u in updated_users_list]
        users_json = json.dumps(users_info)
        with open(self.__file_path, "w") as f:
            f.write(users_json)

    def edit(self, user_id: User.id, username: str):
        current_users = self.get_all()
        if uuid.UUID(hex=user_id) in current_users:
            edited_users = []
            for user in current_users:
                if user.id == uuid.UUID(hex=user_id):
                    user.username = username
                edited_users.append(user)
            users_info = [(str(u.id), u.username, u.stocks) for u in edited_users]
            users_json = json.dumps(users_info)
            with open(self.__file_path, "w") as f:
                f.write(users_json)
