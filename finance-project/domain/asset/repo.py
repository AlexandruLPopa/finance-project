from domain.asset.asset import Asset
from domain.asset.asset_persistence_interface import AssetPersistenceInterface

from domain.user.user import User

# TODO homework
# Refactor this class
# extract the sqlite code from here to the persistence layer
# also create a class which can save these assets in a file with the users -> interface
# this code should have automated tests


class AssetRepo:
    def __init__(self, asset_persistence: AssetPersistenceInterface):
        self.__asset_persistence = asset_persistence
        self.__assets = None

    def add_to_user(self, user: User, asset: Asset):
        self.__asset_persistence.add_to_user(user, asset)
        self.__assets = None
        self.check_we_have_assets(user)

    def get_for_user(self, user: User) -> list[Asset]:
        self.check_we_have_assets(user)
        return self.__assets

    def delete_for_user(self, user: User, asset: Asset):
        self.__asset_persistence.delete_for_user(user, asset)
        self.__assets = None
        self.check_we_have_assets(user)

    def check_we_have_assets(self, user: User):
        if self.__assets is None:
            self.__assets = self.__asset_persistence.get_for_user(user)

#
# class AssetRepo:
#     def add_to_user(self, user: User, asset: Asset):
#         # TODO homework what happens if we already have this asset?
#         # exception, 400 to api already added
#         table = f"{user.id}-assets".replace("-", "_")
#         with sqlite3.connect("main_users.db") as conn:
#             cursor = conn.cursor()
#             try:
#                 cursor.execute(
#                     f"INSERT INTO '{table}' (ticker, name, country, units) "
#                     f"VALUES ('{asset.ticker}', '{asset.name}', "
#                     f"'{asset.country}', {asset.units})"
#                 )
#             except sqlite3.OperationalError:
#                 cursor.execute(
#                     f"CREATE TABLE '{table}' "
#                     f"(ticker TEXT PRIMARY KEY, "
#                     f"name TEXT, country TEXT, units REAL)"
#                 )
#                 cursor.execute(
#                     f"INSERT INTO '{table}' (ticker, name, country, units) "
#                     f"VALUES ('{asset.ticker}', '{asset.name}', "
#                     f"'{asset.country}', {asset.units})"
#                 )
#             conn.commit()
#
#     def get_for_user(self, user: User) -> list[Asset]:
#         table = f"{user.id}-assets".replace("-", "_")
#         with sqlite3.connect("main_users.db") as conn:
#             cursor = conn.cursor()
#             try:
#                 cursor.execute(f"SELECT * FROM '{table}'")
#                 assets_info = cursor.fetchall()
#             except sqlite3.OperationalError as e:
#                 if "no such table" in str(e):
#                     assets_info = []
#                 else:
#                     raise e
#         assets = [
#             Asset(
#                 ticker=x[0],
#                 nr=x[3],
#                 name=x[1],
#                 country=x[2],
#                 sector="sec",
#             )
#             for x in assets_info
#         ]
#         return assets
