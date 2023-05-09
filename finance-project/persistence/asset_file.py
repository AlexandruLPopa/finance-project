import json
import logging
import os
from abc import ABC

from api.users import get_user_by_id, get_all_users
from domain.asset.asset import Asset
from domain.asset.asset_persistence_interface import AssetPersistenceInterface
from domain.asset.factory import AssetFactory
from domain.user.user import User


class AssetPersistenceFile(AssetPersistenceInterface):
    def __init__(self, file_path):
        self.__file_path = file_path

    def add_to_user(self, user_id: str, asset: Asset):
        current_assets = self.get_for_user(user_id)
        current_assets.append(asset)
        current_users = get_all_users()
        assets_info = [(x.ticker, x.units, x.name,
                        x.country, x.current_price, x.currency,
                        x.closed_price, x.fifty_day_price,
                        x.today_low_price, x.today_high_price,
                        x.open_price, x.price_evolution) for x in current_assets]
        updated_users = [[u.id, u.username, u.stocks] if user_id != u.id else
                         [u.id, u.username, assets_info] for u in current_users]
        assets_json = json.dumps(updated_users)
        try:
            with open(self.__file_path, "w") as f:
                f.write(assets_json)
        except Exception as e:
            logging.warning("Could not write to file. Error: " + str(e))

    def get_for_user(self, user_id: str) -> list[Asset]:
        if not os.path.exists(self.__file_path):
            return []
        user = get_user_by_id(user_id)
        return user.stocks

    def delete_for_user(self, user_id: str, asset: Asset):
        try:
            with open(self.__file_path, "r") as file:
                assets_info = json.load(file)
            factory = AssetFactory()
            return [factory.make_new(x) for x in assets_info]
        except Exception as e:
            logging.warning("File could not be read. Error: " + str(e))
            return []
