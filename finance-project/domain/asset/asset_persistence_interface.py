import abc

from domain.user.persistence_interface import UserPersistenceInterface
from domain.asset.asset import Asset
from domain.user.user import User


class AssetPersistenceInterface(UserPersistenceInterface):
    @abc.abstractmethod
    def add_to_user(self, user: User, asset: Asset):
        pass

    @abc.abstractmethod
    def get_for_user(self, user: User) -> list[Asset]:
        pass

    @abc.abstractmethod
    def delete_for_user(self, user: User, asset: Asset):
        pass

    @abc.abstractmethod
    def add(self, user: User):
        pass

    @abc.abstractmethod
    def delete(self, user_id: str):
        pass

    @abc.abstractmethod
    def edit(self, user_id: str, username: str):
        pass

    @abc.abstractmethod
    def get_all(self) -> list[User]:
        pass

