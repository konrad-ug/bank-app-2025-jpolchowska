from src.account import Account

class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"

    def is_nip_valid(self, nip):
        if isinstance(nip, str) and len(nip) == 10 and nip.isdigit():
            return True
        return False
    
    def express_transfer(self, amount: float) -> bool:
        fee = 5.0
        return super().express_transfer(amount, fee)

    def take_loan(self, amount: float):
        if self.balance >= amount * 2 and self.is_transfer_to_ZUS():
            self.balance += amount
            return True
        else:
            return False
    
    def is_transfer_to_ZUS(self):
        for transfer in self.history:
            if transfer == -1775:
                return True
        return False