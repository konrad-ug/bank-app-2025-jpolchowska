import pytest
from src.personal_account import PersonalAccount

@pytest.fixture
def account1():
    acc = PersonalAccount("Jan", "Kowalski", "90000000001")
    acc.balance = 100
    acc.history = [100]
    return acc


@pytest.fixture
def account2():
    acc = PersonalAccount("Anna", "Nowak", "90000000002")
    acc.balance = 200
    acc.history = [200]
    return acc