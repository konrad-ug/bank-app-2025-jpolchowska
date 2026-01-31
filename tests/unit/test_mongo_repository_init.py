from src.mongo_accounts_repository import MongoAccountsRepository

def test_mongo_repository_init_with_mock_collection(mocker):
    mock_collection = mocker.Mock()

    repo = MongoAccountsRepository(collection=mock_collection)

    assert repo.collection is mock_collection
    assert repo._collection is mock_collection
