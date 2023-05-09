import unittest

from domain.user.factory import UserFactory
from domain.user.repo import UserRepo
from persistence.asset_file import AssetPersistenceFile
from persistence.user_file import UserPersistenceFile


class UserRepoTestCase(unittest.TestCase):
    persistence = None
    users_file = "test_users.json"

    @classmethod
    def setUpClass(cls) -> None:
        cls.persistence = UserPersistenceFile(cls.users_file)
        cls.repo = UserRepo(cls.persistence)

    def test_it_deletes_a_user(self):
        expected_username = "random-username"
        new_user = UserFactory().make_new(expected_username)
        self.repo.add(new_user)
        self.repo.delete(str(new_user.id))
        actual_users = [str(u.id) for u in self.repo.get_all()]
        self.assertNotIn(str(new_user.id), actual_users)

    def test_it_edits_a_user(self):
        new_user = UserFactory().make_new("random-username")
        self.repo.add(new_user)
        self.repo.edit(str(new_user.id), "new-username")
        users_list = [x.username for x in self.repo.get_all()]
        self.assertIn("new-username", users_list)

    def test_it_gets_a_user_by_id(self):
        expected_username = "random-username"
        new_user = UserFactory().make_new(expected_username)
        self.repo.add(new_user)
        actual_user = self.repo.get_by_id(str(new_user.id))
        self.assertEqual(expected_username, actual_user.username)

    @classmethod
    def tear_down_class(cls) -> None:
        import os
        os.remove("test_users.json")


if __name__ == "__main__":
    unittest.main()
