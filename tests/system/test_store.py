import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class TestStore(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/store/test_store")

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual({"id": 1, "name": "test_store", "items": []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                response = client.post("/store/test_store")

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(
                    {"message": "A store with name 'test_store' already exists"}, json.loads(response.data)
                )

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                response = client.delete("/store/test_store")

                self.assertEqual(response.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual({"message": "Store deleted"}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                response = client.get("/store/test_store")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"id": 1, "name": "test_store", "items": []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/store/test_store")

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({"message": "Store not found"}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 19.99, 1).save_to_db()
                response = client.get("/store/test_store")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    {"id": 1, "name": "test_store", "items": [{"name": "test_item", "price": 19.99}]}, json.loads(response.data)
                )

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                response = client.get("/stores")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"stores": [{"id": 1, "name": "test_store", "items": []}]}, json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 19.99, 1).save_to_db()
                response = client.get("/stores")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    {"stores": [{"id": 1, "name": "test_store", "items": [{"name": "test_item", "price": 19.99}]}]},
                    json.loads(response.data),
                )
