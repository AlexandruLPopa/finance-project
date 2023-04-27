import unittest
import uuid

from domain.asset.asset import Asset
from domain.user.user import User


class UserMyTestCase(unittest.TestCase):
    def test_user_sets_the_right_username(self):
        # set up
        username = "random_generated"
        user_id = uuid.uuid4()
        user = User(user_id, username)
        # execution
        actual_username = user.username
        # assertion
        self.assertEqual(username, actual_username)

    def test_it_sets_empty_list_if_we_do_not_specify_stock(self):
        user_id = uuid.uuid4()
        username = "random-username"
        user = User(user_id, username)
        actual_stocks = user.stocks
        self.assertEqual([], actual_stocks)

    def test_it_sets_the_stocks_we_give(self):
        user_id = uuid.uuid4()
        username = "random-username"
        test_asset = [Asset(ticker="msft", name="Microsoft", country="United States", nr=0, sector="Tech")]
        user = User(user_id, username, test_asset)
        actual_stocks = user.stocks
        self.assertEqual(test_asset, actual_stocks)

    def test_it_sets_id(self):
        user_id = uuid.uuid4()
        user = User(user_id, "random-username")
        actual_id = user.id
        self.assertEqual(actual_id, user_id)


if __name__ == "__main__":
    unittest.main()
