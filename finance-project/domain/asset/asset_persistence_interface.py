import abc

from domain.user.persistence_interface import UserPersistenceInterface
from domain.asset.asset import Asset
from domain.user.user import User


class AssetPersistenceInterface(UserPersistenceInterface):
    def add_to_user(self, user: User, asset: Asset):
        pass

    def get_for_user(self, user: User) -> list[Asset]:
        pass

    def delete_for_user(self, user: User, asset: Asset):
        pass

    def add(self, user: User):
        pass

    def delete(self, user_id: str):
        pass

    def edit(self, user_id: str, username: str):
        pass

    def get_all_users(self) -> list[User]:
        pass

