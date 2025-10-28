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
    
    def express_transfer(self, amount: float) -> None:
        fee = 5.0
        super().express_transfer(amount, fee)