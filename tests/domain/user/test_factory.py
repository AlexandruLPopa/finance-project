import unittest
import uuid

from domain.user.factory import UserFactory, InvalidUsername
from domain.user.user import User


class UserFactoryTestCase(unittest.TestCase):
    def test_it_creates_a_user_if_the_username_is_between_6_and_20_chars(self):
        username = "between-6-and-20"
        factory = UserFactory()
        actual_user = factory.make_new(username)
        self.assertEqual(username, actual_user.username)
        self.assertEqual(User, type(actual_user))

    def test_it_raises_exception_if_the_username_is_below_6_chars(self):
        username = "below"
        factory = UserFactory()
        with self.assertRaises(InvalidUsername) as context:
            factory.make_new(username)
        self.assertEqual(
            "Username should have at least 6 characters.", str(context.exception)
        )

    def test_it_raises_exception_if_the_username_is_above_20_chars(self):
        username = "usernameabove20characters"
        factory = UserFactory()
        with self.assertRaises(InvalidUsername) as context:
            factory.make_new(username)
        self.assertEqual(
            "Username should have less than 20 characters.", str(context.exception)
        )

    def test_it_creates_a_user_if_the_username_has_valid_chars(self):
        username = "valid-username"
        factory = UserFactory()
        actual_username = factory.make_new(username)
        self.assertEqual(username, actual_username.username)

    def test_it_raises_exception_if_the_username_has_invalid_chars(self):
        username = "invalidusername@"
        factory = UserFactory()
        with self.assertRaises(InvalidUsername) as context:
            factory.make_new(username)
        self.assertEqual(
            "Username should be alphanumeric and can only contain the symbol '-'.", str(context.exception)
        )

    def test_it_makes_user_object_from_persistence(self):
        user_id = "42420b83-0e81-441b-8be0-6e4c469bd363"
        username = "random-username"
        user_info = (user_id, username)
        factory = UserFactory()
        user = factory.make_from_persistence(user_info)
        self.assertIsInstance(user, User)


if __name__ == "__main__":
    unittest.main()
