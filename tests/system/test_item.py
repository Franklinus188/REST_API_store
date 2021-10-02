from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class TestItem(BaseTest):
    def setUp(self):
        super(TestItem, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel("test_user", "1234").save_to_db()
                auth_reuqest = client.post(
                    "/login",
                    data=json.dumps({"username": "test_user", "password": "1234"}),
                    headers={"Content-Type": "application/json"},
                )
                auth_token = json.loads(auth_reuqest.data)["access_token"]
                self.access_token = f"JWT {auth_token}"

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/item/test")
                self.assertEqual(401, response.status_code)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/item/test", headers={"Authorization": self.access_token})
                self.assertEqual(404, response.status_code)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()

                response = client.get("/item/test", headers={"Authorization": self.access_token})
                self.assertEqual(200, response.status_code)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()

                response = client.delete("/item/test")
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({"message": "Item deleted"}, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()

                response = client.post("/item/test", data={"price": 19.99, "store_id": 1})
                self.assertEqual(201, response.status_code)
                self.assertDictEqual({"name": "test", "price": 19.99}, json.loads(response.data))

    def test_create_duplicated_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()

                response = client.post("/item/test", data={"price": 19.99, "store_id": 1})
                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': "An item with name 'test' already exists"}, json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()

                response = client.put("/item/test", data={"price": 19.99, "store_id": 1})
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({"name": "test", "price": 19.99}, json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 9.99, 1).save_to_db()

                self.assertEqual(9.99, ItemModel.find_by_name("test").price)

                response = client.put("/item/test", data={"price": 19.99, "store_id": 1})
                self.assertEqual(200, response.status_code)
                self.assertDictEqual({"name": "test", "price": 19.99}, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test", 19.99, 1).save_to_db()

                response = client.get("/items")

                self.assertDictEqual({"items": [{"name": "test", "price": 19.99}]}, json.loads(response.data))
