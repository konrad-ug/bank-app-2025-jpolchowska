import requests
import pytest

class TestApi:
    url = "http://127.0.0.1:5000"

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        self.person = {
            "name": "Alice",
            "surname": "Smith",
            "pesel": "12345678901"
        }
        response = requests.post(f"{self.url}/api/accounts", json=self.person)
        assert response.status_code == 201
        yield
        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            requests.delete(f"{self.url}/api/accounts/{pesel}")

    def test_create_account(self):
        response = requests.post(f"{self.url}/api/accounts", json=self.person)
        assert response.status_code == 201
        assert response.json()["message"] == "Account created"

    def test_get_all_accounts(self):
        response = requests.get(f"{self.url}/api/accounts")
        assert response.status_code == 200
        assert response.json() == [{"name": "Alice", "surname": "Smith", "pesel":"12345678901", "balance": 0.0}]

    def test_get_account_count(self):
        response = requests.get(f"{self.url}/api/accounts/count")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_get_account_by_pesel(self):
        response = requests.get(f"{self.url}/api/accounts/12345678901")
        assert response.status_code == 200
        assert response.json() == {"name": "Alice", "surname": "Smith", "pesel":"12345678901", "balance": 0.0}

    def test_get_account_by_nonexistent_pesel(self):
        response = requests.get(f"{self.url}/api/accounts/000000000")
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

    def test_update_account(self):
        response = requests.patch(f"{self.url}/api/accounts/12345678901", json = {"name": "Jane"})
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"
        response2 = requests.get(f"{self.url}/api/accounts/12345678901")
        assert response2.json()["name"] == "Jane"
        assert response2.json()["surname"] == "Smith"

    def test_delete_account(self):
        response = requests.delete(f"{self.url}/api/accounts/12345678901")
        assert response.status_code == 200
        assert response.json()["message"] == "Account deleted"
        response2 = requests.get(f"{self.url}/api/accounts/12345678901")
        assert response2.status_code == 404