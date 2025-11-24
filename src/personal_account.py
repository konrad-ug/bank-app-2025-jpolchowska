from src.account import Account

class PersonalAccount(Account):
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

    def express_transfer(self, amount: float) -> None:
        fee = 1.0
        super().express_transfer(amount, fee)