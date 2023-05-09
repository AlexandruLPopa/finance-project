import unittest

from domain.user.factory import UserFactory

from persistence.user_file import UserPersistenceFile


class UserPersistenceFileTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.file_path = "test_users.json"
        cls.repo = UserPersistenceFile(cls.file_path)

    def test_it_adds_a_user(self):
        expected_users_count = len(self.repo.get_all_users()) + 1
        expected_username = "random-username"
        new_user = UserFactory().make_new(expected_username)
        self.repo.add(new_user)
        actual_users = self.repo.get_all_users()
        actual_users_count = len(actual_users)
        self.assertEqual(expected_users_count, actual_users_count)
        self.assertEqual(expected_username, actual_users[-1].username)

    def test_it_reads_users_from_the_system(self):
        expected_username = "random-username"
        new_user = UserFactory().make_new(expected_username)
        self.repo.add(new_user)
        actual_users = self.repo.get_all_users()
        self.assertIsNotNone(actual_users)

    def test_it_deletes_user_from_the_system(self):
        expected_username = "random-username"
        new_user = UserFactory().make_new(expected_username)
        self.repo.add(new_user)
        self.repo.delete(str(new_user.id))
        users_list = [str(u.id) for u in self.repo.get_all_users()]
        self.assertNotIn(str(new_user.id), users_list)

    def test_it_updates_a_username_to_file(self):
        new_user = UserFactory().make_new("random-username")
        self.repo.add(new_user)
        self.repo.edit(str(new_user.id), "new-username")
        users_list = [x.username for x in self.repo.get_all_users()]
        self.assertIn("new-username", users_list)


if __name__ == "__main__":
    unittest.main()
