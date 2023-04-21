import logging
import uuid
from singleton import singleton
from domain.asset.repo import AssetRepo
from domain.user.persistence_interface import UserPersistenceInterface
from domain.user.user import User


class UserIDNotFound(Exception):
    pass


logging.basicConfig(
    filename="finance.log",
    level=logging.DEBUG,
    format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
)


@singleton
class UserRepo:
    def __init__(self, persistence: UserPersistenceInterface):
        print("Initializing user repo")
        self.__persistence = persistence
        self.__users = None

    def add(self, new_user: User):
        self.__persistence.add(new_user)
        self.__users = None
        self.check_users_not_none()

    def edit_by_id(self, user_id: User.id, username: str):
        self.check_users_not_none()
        for u in self.__users:
            if user_id == u.id:
                u.username = username
        self.__persistence.edit_by_id(user_id, username)
        self.__users = None
        self.check_users_not_none()

    def delete_by_id(self, user_id: User.id):
        self.check_users_not_none()
        self.__persistence.delete_by_id(user_id)
        if str(user_id) not in [str(u.id) for u in self.__users]:
            raise UserIDNotFound("The specified user ID does not exist.")
        else:
            for u in self.__users:
                if user_id == u.id:
                    self.__users.remove(u)
            self.__users = None
            self.check_users_not_none()
        logging.info(f"The user with ID {user_id} was deleted.")

    def get_all(self) -> list[User]:
        self.check_users_not_none()
        return self.__users

    def get_by_username(self, username) -> User:
        self.check_users_not_none()
        for u in self.__users:
            if u.username == username:
                return u

    def get_by_id(self, user_id) -> User:
        self.check_users_not_none()
        for u in self.__users:
            if u.id == uuid.UUID(hex=user_id):
                assets = AssetRepo().get_for_user(u)
                return User(uuid=u.id, username=u.username, stocks=assets)

    def check_users_not_none(self):
        if self.__users is None:
            self.__users = self.__persistence.get_all()
