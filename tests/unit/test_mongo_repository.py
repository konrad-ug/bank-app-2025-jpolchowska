from src.mongo_accounts_repository import MongoAccountsRepository

def test_save_all_uses_delete_and_update(mocker, account1):
    mock_collection = mocker.Mock()

    repo = MongoAccountsRepository(collection=mock_collection)
    repo.save_all([account1])

    mock_collection.delete_many.assert_called_once_with({})
    mock_collection.update_one.assert_called_once()


def test_load_all_returns_accounts(mocker, account1, account2):
    mock_collection = mocker.Mock()
    mock_collection.find.return_value = [
        account1.to_dict(),
        account2.to_dict()
    ]

    repo = MongoAccountsRepository(collection=mock_collection)
    accounts = repo.load_all()

    assert len(accounts) == 2
    assert accounts[0].pesel == account1.pesel
    assert accounts[1].pesel == account2.pesel