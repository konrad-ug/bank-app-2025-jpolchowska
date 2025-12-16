from src.accounts_registry import AccountsRegistry
from src.personal_account import PersonalAccount
import pytest

class TestAccountsRegistry:

    @pytest.fixture(autouse=True)
    def registry(self):
        self.registry = AccountsRegistry()

    @pytest.fixture(autouse=True)
    def account1(self):
        self.account1 = PersonalAccount("John", "Doe", "85111100165")

    @pytest.fixture(autouse=True)
    def account2(self):
        self.account2 = PersonalAccount("Jane", "Doe", "85050512345")

    def test_add_account_correct(self):
        result = self.registry.add_account(self.account1)
        assert result is True
        assert self.registry.get_account_count() == 1
        assert self.registry.accounts[0] == self.account1

    def test_get_account_by_pesel_correct(self):
        self.registry.accounts = [self.account1]
        assert self.registry.get_account_by_pesel("85111100165") == self.account1
        assert self.registry.get_account_by_pesel("85050512345") == None

    def test_get_all_accounts_correct(self):
        self.registry.accounts = [self.account1, self.account2]
        assert self.registry.get_all_accounts() == [self.account1, self.account2]

    def test_get_account_count_correct(self):
        self.registry.accounts = [self.account1, self.account2]
        assert self.registry.get_account_count() == 2

    def test_delete_account_existing_pesel(self):
        self.registry.accounts = [self.account1, self.account2]
        self.registry.delete_account("85111100165")
        assert self.registry.get_account_count() == 1
        assert self.registry.get_account_by_pesel("85111100165") == None
        assert self.registry.get_account_by_pesel("85050512345") == self.account2

    def test_delete_account_nonexistent_pesel(self):
        self.registry.accounts = [self.account1]
        self.registry.delete_account("00000000000")
        assert self.registry.get_account_count() == 1
        assert self.registry.accounts[0] == self.account1

    def test_add_account_duplicate_pesel(self):
        self.registry.add_account(self.account1)
        result = self.registry.add_account(self.account1)
        assert result is False
        assert self.registry.get_account_count() == 1