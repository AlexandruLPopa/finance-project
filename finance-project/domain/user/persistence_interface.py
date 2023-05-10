import abc

from domain.asset.asset import Asset
from domain.user.user import User


class UserPersistenceInterface(abc.ABC):
    @abc.abstractmethod
    def add(self, user: User):
        pass

    @abc.abstractmethod
    def get_all_users(self) -> list[User]:
        pass

    # DONE homework: delete & edit

    @abc.abstractmethod
    def edit(self, user_id: str, username: str):
        pass

    @abc.abstractmethod
    def delete(self, user_id: str):
        pass

    @abc.abstractmethod
    def add_to_user(self, user_id: str, ticker: str):
        pass

    @abc.abstractmethod
    def get_for_user(self, user_id: str) -> list[Asset]:
        pass

    @abc.abstractmethod
    def delete_for_user(self, user_id: str, ticker: str):
        pass
