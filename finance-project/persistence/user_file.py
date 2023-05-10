import json
import logging
import os
import uuid

from domain.asset.asset import Asset
from domain.asset.factory import AssetFactory
from domain.user.factory import UserFactory
from domain.user.persistence_interface import UserPersistenceInterface
from domain.user.user import User

logging.basicConfig(
        filename="finance.log",
        level=logging.DEBUG,
        format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
    )


class FailedToAccessPersistence(Exception):
    pass


class UserPersistenceFile(UserPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def get_all_users(self) -> list[User]:
        if not os.path.exists(self.__file_path):
            return []
        try:
            # DONE refactor with
            with open(self.__file_path) as file:
                contents = file.read()
                users_info = json.loads(contents)
                factory = UserFactory()
            return [factory.make_from_persistence(x) for x in users_info]
        except FailedToAccessPersistence as e:
            # DONE homework, log error
            logging.error("Could not read file, reason: " + str(e))
            return []

    def add(self, user: User):
        current_users = self.get_all_users()
        current_users.append(user)
        users_info = [(str(u.id), u.username, u.stocks) for u in current_users]
        users_json = json.dumps(users_info)
        # DONE homework refactor with
        try:
            with open(self.__file_path, "w") as file:
                file.write(users_json)
        except FailedToAccessPersistence as e:
            logging.error("Could not write user info to persistence. Error: " + str(e))
            raise e

    def delete(self, user_id: User.id):
        current_users = self.get_all_users()
        updated_users_list = [u for u in current_users if str(u.id) != user_id]
        users_info = [(str(u.id), u.username, u.stocks) for u in updated_users_list]
        users_json = json.dumps(users_info)
        try:
            with open(self.__file_path, "w") as file:
                file.write(users_json)
        except FailedToAccessPersistence as e:
            logging.error("Could not delete user info from persistence. Error: " + str(e))
            raise e

    def edit(self, user_id: User.id, username: str):
        current_users = self.get_all_users()
        updated_users = [(str(u.id), username, u.stocks) if str(u.id) == user_id
                         else (str(u.id), u.username, u.stocks) for u in current_users]
        users_json = json.dumps(updated_users)
        try:
            with open(self.__file_path, "w") as f:
                f.write(users_json)
        except FailedToAccessPersistence as e:
            logging.error("Could not write user info to persistence. Error: " + str(e))
            raise e

    def add_to_user(self, user_id: str, asset: Asset):
        current_assets = self.get_for_user(user_id)
        current_assets.append(asset)
        current_users = self.get_all_users()
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
        current_users = self.get_all_users()
        user = [u for u in current_users if user_id == str(u.id)][0]
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
