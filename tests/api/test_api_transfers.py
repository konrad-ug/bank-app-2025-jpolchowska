import requests
import pytest

class TestApiTransfers:
    url = "http://127.0.0.1:5000"

    @pytest.fixture(autouse=True)
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

    def test_incoming_transfer_successful(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)

        response = requests.post(
            f"{self.url}/api/accounts/{person['pesel']}/transfer",
            json={"amount": 500, "type": "incoming"}
        )
        assert response.status_code == 200

        account = requests.get(
            f"{self.url}/api/accounts/{person['pesel']}"
        ).json()
        assert account["balance"] == 500.0

    def test_outgoing_transfer_successful(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)

        requests.post(
            f"{self.url}/api/accounts/{person['pesel']}/transfer",
            json={"amount": 1000, "type": "incoming"}
        )

        response = requests.post(
            f"{self.url}/api/accounts/{person['pesel']}/transfer",
            json={"amount": 300, "type": "outgoing"}
        )
        assert response.status_code == 200

        account = requests.get(
            f"{self.url}/api/accounts/{person['pesel']}"
        ).json()
        assert account["balance"] == 700.0

    def test_outgoing_transfer_insufficient_funds(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)

        response = requests.post(
            f"{self.url}/api/accounts/{person['pesel']}/transfer",
            json={"amount": 100, "type": "outgoing"}
        )
        assert response.status_code == 422

    def test_express_transfer_insufficient_funds(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)

        response = requests.post(
            f"{self.url}/api/accounts/{person['pesel']}/transfer",
            json={"amount": 100, "type": "express"}
        )
        assert response.status_code == 422

    def test_transfer_unknown_type(self, person):
        requests.post(f"{self.url}/api/accounts", json=person)

        response = requests.post(
            f"{self.url}/api/accounts/{person['pesel']}/transfer",
            json={"amount": 100, "type": "crypto"}
        )
        assert response.status_code == 400