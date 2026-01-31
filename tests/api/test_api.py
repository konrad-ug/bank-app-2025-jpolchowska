import requests
import pytest

class TestApi:
    url = "http://127.0.0.1:5000"

    @pytest.fixture(autouse=True, scope="function")
    def cleanup(self):
        yield
        response = requests.get(f"{self.url}/api/accounts")
        if response.status_code == 200:
            for account in response.json():
                requests.delete(f"{self.url}/api/accounts/{account['pesel']}")

    @pytest.fixture
    def person(self):
        return {
            "name": "Alice",
            "surname": "Smith",
            "pesel": "12345678901"
        }

    def test_create_account(self, person):
        response = requests.post(f"{self.url}/api/accounts", json=person)
        assert response.status_code == 201
        assert response.json()["message"] == "Account created"

    def test_get_all_accounts(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)
        response = requests.get(f"{self.url}/api/accounts")
        assert response.status_code == 200
        assert response.json() == [{
            "name": "Alice",
            "surname": "Smith",
            "pesel": "12345678901",
            "balance": 0.0
        }]

    def test_get_account_count(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)
        response = requests.get(f"{self.url}/api/accounts/count")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_get_account_by_pesel(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)
        response = requests.get(f"{self.url}/api/accounts/12345678901")
        assert response.status_code == 200

    def test_get_account_by_nonexistent_pesel(self):
        response = requests.get(f"{self.url}/api/accounts/000000000")
        assert response.status_code == 404

    def test_update_account(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)
        response = requests.patch(
            f"{self.url}/api/accounts/12345678901",
            json={"name": "Jane"}
        )
        assert response.status_code == 200

    def test_delete_account(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)
        response = requests.delete(f"{self.url}/api/accounts/12345678901")
        assert response.status_code == 200

    def test_create_account_with_existing_pesel(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)
        response = requests.post(f"{self.url}/api/accounts", json=person)
        assert response.status_code == 409