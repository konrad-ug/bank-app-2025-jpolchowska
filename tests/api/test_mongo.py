import requests
import pytest

class TestSaveLoadApi:

    @pytest.fixture(autouse=True)
    def base_data(self):
        self.url = "http://127.0.0.1:5000"
        self.account_data = {
            "name": "Anna",
            "surname": "Nowak",
            "pesel": "11223344556"
        }

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        response = requests.post(
            f"{self.url}/api/accounts",
            json=self.account_data
        )
        assert response.status_code == 201

        requests.post(
            f"{self.url}/api/accounts/{self.account_data['pesel']}/transfer",
            json={"amount": 1000, "type": "incoming"}
        )

        yield

        response = requests.get(f"{self.url}/api/accounts")
        for account in response.json():
            requests.delete(f"{self.url}/api/accounts/{account['pesel']}")

    def test_save_and_load_accounts(self):
        response = requests.post(f"{self.url}/api/accounts/save")
        assert response.status_code == 200

        response = requests.get(f"{self.url}/api/accounts")
        for account in response.json():
            requests.delete(f"{self.url}/api/accounts/{account['pesel']}")

        response = requests.post(f"{self.url}/api/accounts/load")
        assert response.status_code == 200

        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()

        assert len(accounts) == 1
        assert accounts[0]["pesel"] == self.account_data["pesel"]
        assert accounts[0]["balance"] == 1000
        assert accounts[0]["name"] == self.account_data["name"]
        assert accounts[0]["surname"] == self.account_data["surname"]