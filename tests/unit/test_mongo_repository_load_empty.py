from src.mongo_accounts_repository import MongoAccountsRepository

def test_load_all_when_collection_empty(mocker):
    mock_collection = mocker.Mock()
    mock_collection.find.return_value = []

    repo = MongoAccountsRepository(collection=mock_collection)
    accounts = repo.load_all()

    assert accounts == []