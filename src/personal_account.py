from src.account import Account
from datetime import date
from smtp.smtp import SMTPClient

class PersonalAccount(Account):
    history_email_text_template = "Personal account history: {}"

    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.promo_code = promo_code
        if self.is_promo_code_valid(promo_code) and self.yob_from_pesel() > 1960:
            self.balance = 50.0
        else:
            self.balance = 0.0
        
    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11 and pesel.isdigit():
            return True
        return False
        
    def is_promo_code_valid(self, promo_code):
        if promo_code is None:
            return False
        if promo_code.startswith("PROM_") and len(promo_code) == 8:
            return True
        return False
    
    def yob_from_pesel(self):
        pesel = self.pesel
        if pesel.isdigit():
            year = int(pesel[:2])
            month = int(pesel[2:4])
            if 1 <= month <= 12:
                return 1900 + year
            elif 21 <= month <= 32:
                return 2000 + year
        else:
            return 0

    def express_transfer(self, amount: float) -> bool:
        fee = 1.0
        return super().express_transfer(amount, fee)

    def submit_for_loan(self, amount: float):
        length = len(self.history)
        # WARUNEK 1 - ostatnie trzy transakcje są dodatnie
        if length >= 3 and self.are_last_three_positive():
            self.balance += amount
            return True
        # WARUNEK 2 - suma ostatnich pięciu transakcji > amount
        if length >= 5 and self.is_sum_of_last_five_greater_than_amount(amount):
            self.balance += amount
            return True
        return False
    
    def are_last_three_positive(self):
        if self.history[-1] > 0 and self.history[-2] > 0 and self.history[-3] > 0:
            return True
        else:
            return False
        
    def is_sum_of_last_five_greater_than_amount(self, amount):
        last_five_sum = self.history[-5] + self.history[-4] + self.history[-3] + self.history[-2] + self.history[-1]
        if last_five_sum > amount:
            return True
        else:
            return False
        
    def send_history_via_email(self, email_address: str) -> bool:
        today_date = date.today().strftime("%Y-%m-%d")
        subject = "Account Transfer History " + today_date
        text = self.history_email_text_template.format(self.history)
        return SMTPClient.send(subject, text, email_address)
    
    def to_dict(self):
        return {
            "first name": self.first_name,
            "last_name": self.last_name,
            "pesel": self.pesel,
            "balance": self.balance,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(
            data.get("first_name"),
            data.get("last_name"),
            data.get("pesel"),
        )
        account.balance = data.get("balance", account.balance)
        account.history = data.get("history", [])
        return account