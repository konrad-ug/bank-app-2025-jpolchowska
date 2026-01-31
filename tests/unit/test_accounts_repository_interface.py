import pytest
from src.accounts_repository_interface import AccountsRepository

def test_accounts_repository_is_abstract():
    with pytest.raises(TypeError):
        AccountsRepository()

class DummyRepository(AccountsRepository):
    def save_all(self, accounts: list):
        return "saved"

    def load_all(self) -> list:
        return []

def test_accounts_repository_interface_methods_are_callable():
    repo = DummyRepository()

    assert repo.save_all([]) == "saved"
    assert repo.load_all() == []