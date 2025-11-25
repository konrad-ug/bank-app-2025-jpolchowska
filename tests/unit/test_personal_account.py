from src.personal_account import PersonalAccount
import pytest

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

    def test_yob_from_pesel_before_2000(self):
        account = PersonalAccount("John", "Doe", "85050512345")
        assert account.yob_from_pesel() == 1985

    def test_yob_from_pesel_post_2000(self):
        account = PersonalAccount("John", "Doe", "01210112345")
        assert account.yob_from_pesel() == 2001

    def test_yob_from_pesel_invalid(self):
        account = PersonalAccount("Bob", "Doe", "1234567ABCD")
        assert account.yob_from_pesel() == 0


class TestLoan:

    @pytest.fixture(autouse=True)
    def account(self):
        self.account = PersonalAccount("John", "Doe", "85111100165")

    @pytest.mark.parametrize(
        "history, amount, expected_result, expected_balance",
        [
            ([50, 30, 100], 30, True, 30),
            ([50.0, 30.0, 40.0, -10.0, -10.0], 30, True, 30),
            ([40], 30, False, 0),
            ([10.0, 10.0, -20.0], 30, False, 0),
            ([-10.0, -10.0, -20.0, 10.0, 10.0], 30, False, 0),
            ([50.0, -10.0, -20.0, -10.0, 10.0], 30, False, 0),
        ],
        ids=[
            "three positives",
            "five with sum greater than zero",
            "one positive",
            "three but one negative",
            "five with sum less than zero",
            "five but sum lesser than requested amount"
        ]
    )

    def test_loan(self, history, amount, expected_result, expected_balance):
        self.account.history = history
        result = self.account.submit_for_loan(amount)
        assert result == expected_result
        assert self.account.balance == expected_balance