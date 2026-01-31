import pytest
import requests
import uuid

class TestAPIMongo:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.url = "http://127.0.0.1:5000/api/accounts"

        # unikalne pesele – brak kolizji między testami
        self.person1 = {
            "name": "Jane",
            "surname": "Doe",
            "pesel": "9" + uuid.uuid4().hex[:10]
        }
        self.person2 = {
            "name": "John",
            "surname": "Doe",
            "pesel": "8" + uuid.uuid4().hex[:10]
        }

    def test_create_save_and_load(self):
        # create
        requests.post(self.url, json=self.person1)
        requests.post(self.url, json=self.person2)

        # save to mongo
        resp = requests.post(f"{self.url}/save")
        assert resp.status_code == 200

        # clear registry by restarting state via load
        resp = requests.post(f"{self.url}/load")
        assert resp.status_code == 200

        # verify
        response = requests.get(self.url)
        assert response.status_code == 200

        pesels = {acc["pesel"] for acc in response.json()}
        assert self.person1["pesel"] in pesels
        assert self.person2["pesel"] in pesels

    def test_load_without_save_does_not_add_new_accounts(self):
        # create accounts, but DO NOT save
        requests.post(self.url, json=self.person1)
        requests.post(self.url, json=self.person2)

        # load from mongo (should load only what was previously saved)
        resp = requests.post(f"{self.url}/load")
        assert resp.status_code == 200

        response = requests.get(self.url)
        assert response.status_code == 200

        pesels = {acc["pesel"] for acc in response.json()}

        # accounts from THIS test should NOT magically appear in mongo
        assert self.person1["pesel"] not in pesels
        assert self.person2["pesel"] not in pesels