from src.mongo_accounts_repository import MongoAccountsRepository
from src.personal_account import PersonalAccount

def test_save_all_clears_and_saves_accounts(mocker):
    mock_collection = mocker.Mock()

    repo = MongoAccountsRepository(collection=mock_collection)

    acc1 = PersonalAccount("Jan", "Kowalski", "90000000001")
    acc2 = PersonalAccount("Anna", "Nowak", "90000000002")

    repo.save_all([acc1, acc2])

    mock_collection.delete_many.assert_called_once_with({})
    assert mock_collection.update_one.call_count == 2


def test_load_all_returns_accounts(mocker):
    mock_collection = mocker.Mock()

    mock_collection.find.return_value = [
        {
            "first_name": "Jan",
            "last_name": "Kowalski",
            "pesel": "90000000001",
            "balance": 100,
            "history": [100]
        },
        {
            "first_name": "Anna",
            "last_name": "Nowak",
            "pesel": "90000000002",
            "balance": 0,
            "history": []
        }
    ]

    repo = MongoAccountsRepository(collection=mock_collection)

    accounts = repo.load_all()

    assert len(accounts) == 2
    assert accounts[0].first_name == "Jan"
    assert accounts[1].pesel == "90000000002"