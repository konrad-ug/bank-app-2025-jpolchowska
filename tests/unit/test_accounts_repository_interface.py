import pytest
from src.accounts_repository_interface import AccountsRepository


def test_accounts_repository_is_abstract():
    with pytest.raises(TypeError):
        AccountsRepository()