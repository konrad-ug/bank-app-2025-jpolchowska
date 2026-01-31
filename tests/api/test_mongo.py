import pytest
import requests
from src.mongo_accounts_repository import MongoAccountsRepository


class TestAPIMongo:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = "http://127.0.0.1:5000/api/accounts"
        self.person1 = {
            "name": "Jane",
            "surname": "Doe",
            "pesel": "06210802343"
        }
        self.person2 = {
            "name": "John",
            "surname": "Doe",
            "pesel": "05210802343"
        }

    def test_create_save_delete_load(self):
        requests.post(f"{self.url}/clear")
        MongoAccountsRepository().collection.delete_many({})

        requests.post(self.url, json=self.person1)
        requests.post(self.url, json=self.person2)

        requests.post(f"{self.url}/save")
        requests.post(f"{self.url}/clear")
        requests.post(f"{self.url}/load")

        response = requests.get(self.url)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_create_delete_load_no_save(self):
        requests.post(f"{self.url}/clear")
        MongoAccountsRepository().collection.delete_many({})

        requests.post(self.url, json=self.person1)
        requests.post(self.url, json=self.person2)

        requests.post(f"{self.url}/clear")
        requests.post(f"{self.url}/load")

        response = requests.get(self.url)
        assert response.status_code == 200
        assert len(response.json()) == 0