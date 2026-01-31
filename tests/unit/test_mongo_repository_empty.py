from src.mongo_accounts_repository import MongoAccountsRepository

def test_save_all_with_empty_accounts_list(mocker):
    mock_collection = mocker.Mock()

    repo = MongoAccountsRepository(collection=mock_collection)
    repo.save_all([])

    mock_collection.delete_many.assert_called_once_with({})
    mock_collection.update_one.assert_not_called()