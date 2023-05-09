import abc

from domain.user.persistence_interface import UserPersistenceInterface
from domain.asset.asset import Asset


class AssetPersistenceInterface(UserPersistenceInterface):
    @abc.abstractmethod
    def add_to_user(self, user_id: str, asset: Asset):
        pass

    @abc.abstractmethod
    def get_for_user(self) -> list[Asset]:
        pass

    @abc.abstractmethod
    def delete_for_user(self, user_id: str, asset: Asset):
        pass
