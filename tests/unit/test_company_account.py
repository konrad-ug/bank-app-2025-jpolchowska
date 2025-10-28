from src.company_account import CompanyAccount

class TestCompanyAccount:
    def test_account_creation(self):
        account = CompanyAccount("Tech Solutions", "1234567890")
        assert account.company_name == "Tech Solutions"
        assert account.nip == "1234567890"

    def test_account_creation_with_invalid_nip_too_short(self):
        account = CompanyAccount("Business Corp", "12345")
        assert account.nip == "Invalid"

    def test_account_creation_with_invalid_nip_too_long(self):
        account = CompanyAccount("Tech Solutions", "1234567891011")
        assert account.nip == "Invalid"
    
    def test_account_creation_with_invalid_nip_with_letters(self):
        account = CompanyAccount("Tech Solutions", "123A56B89C")
        assert account.nip == "Invalid"

    def test_account_creation_with_invalid_nip_empty(self):
        account = CompanyAccount("Tech Solutions", "")
        assert account.nip == "Invalid"