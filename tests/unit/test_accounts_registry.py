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
        self.registry.add_account(self.account1)
        assert self.registry.accounts[-1] == self.account1

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