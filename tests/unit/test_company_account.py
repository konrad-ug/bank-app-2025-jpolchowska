from src.company_account import CompanyAccount
import pytest

class TestCompanyAccount:
    def test_invalid_nip_no_request(self, mocker):
        mock_get = mocker.patch("src.company_account.requests.get")
        account = CompanyAccount("Tech Solutions", "123")
        assert account.nip == "Invalid"
        mock_get.assert_not_called()

    def test_active_company(self, mocker):
        mocker.patch(
            "src.company_account.requests.get",
            return_value=mocker.Mock(
                json=lambda: {
                    "result": {
                        "subject": {
                            "statusVat": "Czynny"
                        }
                    }
                }
            )
        )

        account = CompanyAccount("Tech Solutions", "1234567890")
        assert account.nip == "1234567890"

    def test_inactive_company_raises_error(self, mocker):
        mocker.patch(
            "src.company_account.requests.get",
            return_value=mocker.Mock(
                json=lambda: {
                    "result": {
                        "subject": {
                            "statusVat": "Zwolniony"
                        }
                    }
                }
            )
        )

        with pytest.raises(ValueError):
            CompanyAccount("Tech Solutions", "1234567890")

class TestLoan:

    @pytest.fixture(autouse=True)
    def account(self, mocker):
        mocker.patch(
            "src.company_account.CompanyAccount.verify_nip",
            return_value=True
        )
        self.account = CompanyAccount("Tech Solutions", "1234567890")
    
    @pytest.mark.parametrize(
        "history, balance, amount, expected_result, expected_balance",
        [
            ([100, -1775, -50], 60, 30, True, 90),
            ([100, 50, -50], 100, 30, False, 100),
            ([100, -1775, -50], 50, 30, False, 50),
            ([150, -50, -50], 50, 200, False, 50)
        ],
        ids=[
            "balance at least 2x greater than amount and transfer to ZUS",
            "balance at least 2x greater than amount and no transfer to ZUS",
            "balance is not at least 2x greater than amount and transfer to ZUS",
            "balance is not at least 2x greater than amount and no transfer to ZUS"
        ]
    )

    def test_loan(self, history, balance, amount, expected_result, expected_balance):
        self.account.history = history
        self.account.balance = balance
        result = self.account.take_loan(amount)
        assert result == expected_result
        assert self.account.balance == expected_balance