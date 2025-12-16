import requests
import pytest

class TestApiTransfers:
    url = "http://127.0.0.1:5000"

    @pytest.fixture(autouse=True)
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

    def test_incoming_transfer_successful(self):
        response = requests.post(
            f"{self.url}/api/accounts/{self.person['pesel']}/transfer",
            json={"amount": 500, "type": "incoming"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Transfer successful"
        account = requests.get(
            f"{self.url}/api/accounts/{self.person['pesel']}"
        ).json()
        assert account["balance"] == 500.0

    def test_outgoing_transfer_successful(self):
        requests.post(
            f"{self.url}/api/accounts/{self.person['pesel']}/transfer",
            json={"amount": 1000, "type": "incoming"}
        )
        response = requests.post(
            f"{self.url}/api/accounts/{self.person['pesel']}/transfer",
            json={"amount": 300, "type": "outgoing"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Transfer successful"
        account = requests.get(
            f"{self.url}/api/accounts/{self.person['pesel']}"
        ).json()
        assert account["balance"] == 700.0

    def test_outgoing_transfer_insufficient_funds(self):
        response = requests.post(
            f"{self.url}/api/accounts/{self.person['pesel']}/transfer",
            json={"amount": 100, "type": "outgoing"}
        )
        assert response.status_code == 422
        assert response.json()["message"] == "Transfer rejected - insufficient funds"

    def test_express_transfer_insufficient_funds(self):
        response = requests.post(
            f"{self.url}/api/accounts/{self.person['pesel']}/transfer",
            json={"amount": 100, "type": "express"}
        )
        assert response.status_code == 422
        assert response.json()["message"] == "Transfer rejected - insufficient funds"

    def test_transfer_unknown_type(self):
        response = requests.post(
            f"{self.url}/api/accounts/{self.person['pesel']}/transfer",
            json={"amount": 100, "type": "crypto"}
        )
        assert response.status_code == 400
        assert response.json()["message"] == "Unknown transfer type"