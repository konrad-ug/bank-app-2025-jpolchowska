import requests
import pytest

class TestSaveLoadApi:

    @pytest.fixture(autouse=True, scope="function")
    def setup_method(self):
        # Create account
        response = requests.post(
            f"{self.url}/api/accounts",
            json=self.account_data
        )
        assert response.status_code == 201

        # Make a transfer
        requests.post(
            f"{self.url}/api/accounts/{self.account_data['pesel']}/transfer",
            json={"amount": 1000}
        )

        yield

        # Cleanup – delete all accounts
        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            requests.delete(f"{self.url}/api/accounts/{pesel}")

    def test_save_and_load_accounts(self):
        # Save accounts to MongoDB
        response = requests.post(f"{self.url}/api/accounts/save")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Accounts saved to MongoDB"

        # Delete all accounts from registry
        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()
        for account in accounts:
            pesel = account["pesel"]
            requests.delete(f"{self.url}/api/accounts/{pesel}")

        # Load accounts from MongoDB
        response = requests.post(f"{self.url}/api/accounts/load")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Accounts loaded from MongoDB"

        # Verify the account is back in the registry
        response = requests.get(f"{self.url}/api/accounts")
        accounts = response.json()

        assert len(accounts) == 1
        assert accounts[0]["pesel"] == self.account_data["pesel"]
        assert accounts[0]["balance"] == 1000
        assert accounts[0]["name"] == self.account_data["name"]
        assert accounts[0]["surname"] == self.account_data["surname"]