from src.personal_account import PersonalAccount

class TestPersonalAccount:
    def test_personal_account_creation(self):
        account = PersonalAccount("John", "Doe", "85111100165")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "85111100165"
        assert account.promo_code == None

    # Testy PESEL

    def test_pesel_empty(self):
        account = PersonalAccount("John", "Doe", "")
        assert account.pesel == "Invalid"

    def test_pesel_none(self):
        account = PersonalAccount("John", "Doe", None)
        assert account.pesel == "Invalid"

    def test_pesel_too_long(self):
        account = PersonalAccount("John", "Doe", "1234567891011")
        assert account.pesel == "Invalid"

    def test_pesel_too_short(self):
        account = PersonalAccount("John", "Doe", "12345")
        assert account.pesel == "Invalid"

    def test_pesel_not_numeric(self):
        account = PersonalAccount("John", "Doe", "12345ABCDEF")
        assert account.pesel == "Invalid"

    def test_pesel_only_letters(self):
        account = PersonalAccount("John", "Doe", "abcdefghijk")
        assert account.pesel == "Invalid"

    # Testy promo_code

    def test_promo_code_valid_numbers(self):
        account = PersonalAccount("John", "Doe", "85111100165", "PROM_123")
        assert account.balance == 50.0

    def test_promo_code_valid_letters(self):
        account = PersonalAccount("John", "Doe", "85111100165", "PROM_ABC")
        assert account.balance == 50.0

    def test_promo_code_none(self):
        account = PersonalAccount("John", "Doe", "85111100165")
        assert account.balance == 0.0

    def test_promo_code_wrong_prefix(self):
        account = PersonalAccount("John", "Doe", "85111100165", "PAOM_123")
        assert account.balance == 0.0
    
    def test_promo_code_wrong_sufix_too_long(self):
        account = PersonalAccount("John", "Doe", "85111100165", "PROM_1234")
        assert account.balance == 0.0

    def test_promo_code_wrong_sufix_too_short(self):
        account = PersonalAccount("John", "Doe", "85111100165", "PROM_12")
        assert account.balance == 0.0

    # Testy promo_code + yob

    def test_promo_code_before_1960(self):
        account = PersonalAccount("John", "Doe", "55010100123", "PROM_123")
        assert account.balance == 0.0

    def test_promo_code_1960(self):
        account = PersonalAccount("John", "Doe", "60060600123", "PROM_123")
        assert account.balance == 0.0

    def test_promo_code_after_1960(self):
        account = PersonalAccount("John", "Doe", "85111100165", "PROM_123")
        assert account.balance == 50.0