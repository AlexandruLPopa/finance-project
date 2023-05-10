import logging
import uuid

from domain.asset.asset import Asset
from singleton import singleton
from domain.user.persistence_interface import UserPersistenceInterface
from domain.user.user import User

logging.basicConfig(
        filename="finance.log",
        level=logging.DEBUG,
        format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
    )


class UserIDNotFound(Exception):
    pass


@singleton
class UserRepo:
    def __init__(self, persistence: UserPersistenceInterface):
        print("Initializing user repo")
        self.__persistence = persistence
        self.__users = None
        self.__stocks = []

    def add(self, new_user: User):
        self.__persistence.add(new_user)
        self.__users = None
        self.check_users_not_none()
        logging.info(f"The user {new_user.username} was successfully created.")

    def edit(self, user_id: User.id, username: str):
        self.check_users_not_none()
        self.check_id_exists(user_id)
        for u in self.__users:
            if user_id == u.id:
                u.username = username
        self.__persistence.edit(user_id, username)
        self.__users = None
        self.check_users_not_none()
        logging.info(f"The user with ID {user_id} was changed to {username}.")

    def delete(self, user_id: User.id):
        self.check_users_not_none()
        self.check_id_exists(user_id)
        for u in self.__users:
            if user_id == u.id:
                self.__users.remove(u)
        self.__persistence.delete(user_id)
        self.__users = None
        self.check_users_not_none()
        logging.info(f"The user with ID {user_id} was deleted.")

    def get_all_users(self) -> list[User]:
        self.check_users_not_none()
        return self.__users

    def get_by_id(self, user_id: User.id) -> User:
        self.check_users_not_none()
        self.check_id_exists(user_id)
        for u in self.__users:
            if str(u.id) == str(user_id):
                stocks = self.__persistence.get_for_user(u)
                return User(uuid=u.id, username=u.username, stocks=stocks)

    def check_users_not_none(self):
        if self.__users is None:
            self.__users = self.__persistence.get_all_users()

    def check_id_exists(self, user_id: str):
        if str(user_id) not in [str(u.id) for u in self.__users]:
            logging.error(msg="The specified user ID does not exist.")
            raise UserIDNotFound("The specified user ID does not exist.")

    def add_to_user(self, user_id: str, ticker: str):
        self.__persistence.add_to_user(user_id, ticker)
        self.__stocks = None
        self.check_we_have_assets(user_id)

    def get_for_user(self, user_id: str) -> list[Asset]:
        self.check_we_have_assets(user_id)
        return self.__stocks

    def delete_for_user(self, user_id: str, ticker: str):
        self.__persistence.delete_for_user(user_id, ticker)
        self.__stocks = None
        self.check_we_have_assets(user_id)

    def check_we_have_assets(self, user_id: str):
        if self.__stocks is None:
            self.__stocks = self.__persistence.get_for_user(user_id)
