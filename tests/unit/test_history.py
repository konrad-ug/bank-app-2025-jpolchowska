from src.account import Account

def test_history_create():
    account = Account()
    assert account.history == []

def test_incoming_transfer_history():
    account = Account()
    account.incoming_transfer(500)
    assert account.history == [500]

def test_outgoing_transfer_history():
    account = Account()
    account.incoming_transfer(500)
    account.outgoing_transfer(300)
    assert account.history == [500, -300]

def test_express_transfer_history():
    account = Account()
    account.incoming_transfer(500)
    account.express_transfer(300, 1)
    assert account.history == [500, -300, -1]