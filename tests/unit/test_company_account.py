from src.company_account import CompanyAccount
import pytest

class TestCompanyAccount:
    def test_company_account_creation(self):
        account = CompanyAccount("Tech Solutions", "1234567890")
        assert account.company_name == "Tech Solutions"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_nip_empty(self):
        account = CompanyAccount("Tech Solutions", "")
        assert account.nip == "Invalid"

    def test_nip_none(self):
        account = CompanyAccount("Tech Solutions", None)
        assert account.nip == "Invalid"

    def test_nip_too_short(self):
        account = CompanyAccount("Tech Solutions", "123")
        assert account.nip == "Invalid"

    def test_nip_too_long(self):
        account = CompanyAccount("Tech Solutions", "1234567891011")
        assert account.nip == "Invalid"
    
    def test_nip_with_letters(self):
        account = CompanyAccount("Tech Solutions", "123456789A")
        assert account.nip == "Invalid"

    def test_nip_correct(self):
        account = CompanyAccount("Tech Solutions", "9492458300")
        assert account.nip == "9492458300"

class TestLoan:

    @pytest.fixture(autouse=True)
    def account(self):
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