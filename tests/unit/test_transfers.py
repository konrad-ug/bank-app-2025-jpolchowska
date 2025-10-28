from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestTransfers:
    def test_personal_incoming_transfer_correct(self):
        account = PersonalAccount("Alice", "Johnson", "12345678901")
        account.incoming_transfer(100.0)
        assert account.balance == 100.0

    def test_personal_outgoing_transfer_exceeding_balance(self):
        account = PersonalAccount("Alice", "Johnson", "12345678901")
        account.balance = 80.0
        account.outgoing_transfer(50.0)
        assert account.balance == 30.0

    def test_personal_incoming_transfer_negative_amount(self):
        account = PersonalAccount("Alice", "Johnson", "12345678901")
        account.incoming_transfer(-20.0)
        assert account.balance == 0.0

    def test_personal_outgoing_transfer_correct(self):
        account = PersonalAccount("Alice", "Johnson", "12345678901")
        account.incoming_transfer(100.0)
        account.outgoing_transfer(50.0)
        assert account.balance == 50.0

    def test_personal_express_transfer_correct(self):
        account = PersonalAccount("Alice", "Johnson", "12345678901")
        account.incoming_transfer(50.0)
        account.express_transfer(50.0)
        assert account.balance == -1.0

    def test_personal_express_transfer_too_much(self):
        account = PersonalAccount("Alice", "Johnson", "12345678901")
        account.incoming_transfer(50.0)
        account.express_transfer(100.0)
        assert account.balance == 50.0

    def test_company_incoming_transfer_correct(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.incoming_transfer(200.0)
        assert account.balance == 200.0

    def test_company_outgoing_transfer_correct(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.incoming_transfer(100.0)
        account.outgoing_transfer(40.0)
        assert account.balance == 60.0

    def test_company_express_transfer_correct(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.incoming_transfer(50.0)
        account.express_transfer(50.0)
        assert account.balance == -5.0

    def test_company_express_transfer_too_much(self):
        account = CompanyAccount("TechCorp", "1234567890")
        account.incoming_transfer(50.0)
        account.express_transfer(100.0)
        assert account.balance == 50.0