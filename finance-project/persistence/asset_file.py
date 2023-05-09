from domain.asset.asset import Asset
from domain.asset.asset_persistence_interface import AssetPersistenceInterface


class AssetPersistenceFile(AssetPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def add_to_user(self, user_id: str, asset: Asset):
        pass

    def get_for_user(self) -> list[Asset]:
        pass

    def delete_for_user(self, user_id: str, asset: Asset):
        pass
