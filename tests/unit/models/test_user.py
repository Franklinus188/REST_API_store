from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class TestUser(UnitBaseTest):
    def test_create_user(self):
        user = UserModel("test_user", "test")

        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.password, "test")
