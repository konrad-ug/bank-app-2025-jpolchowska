from src.company_account import CompanyAccount

class TestCompanyAccount:
    def test_company_account_creation(self):
        account = CompanyAccount("Tech Solutions", "1234567890")
        assert account.company_name == "Tech Solutions"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_nip_empty(self):
        account = CompanyAccount("Tech Solutions", "")
        assert account.nip == "Invalid"

    def test_nip_none(self):
        account = CompanyAccount("Tech Solutions", None)
        assert account.nip == "Invalid"

    def test_nip_too_short(self):
        account = CompanyAccount("Tech Solutions", "123")
        assert account.nip == "Invalid"

    def test_nip_too_long(self):
        account = CompanyAccount("Tech Solutions", "1234567891011")
        assert account.nip == "Invalid"
    
    def test_nip_with_letters(self):
        account = CompanyAccount("Tech Solutions", "123456789A")
        assert account.nip == "Invalid"

    def test_nip_correct(self):
        account = CompanyAccount("Tech Solutions", "9492458300")
        assert account.nip == "9492458300"