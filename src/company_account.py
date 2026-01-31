import os
import requests
from datetime import date
from smtp.smtp import SMTPClient

from src.account import Account

class CompanyAccount(Account):
    history_email_text_template = "Company account history: {}"

    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        if not self.is_nip_valid(nip):
            self.nip = "Invalid"
        elif self.verify_nip(nip):
            self.nip = nip
        else:
            raise ValueError("Company not registered!!")

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
    
    def verify_nip(self, nip):
        today = date.today().isoformat()
        base_url = os.getenv("BANK_APP_MF_URL", "https://wl-api.mf.gov.pl")
        url = f"{base_url}/api/search/nip/{nip}?date={today}"

        try:
            response = requests.get(url)
            data = response.json()
            print(f"Response for NIP {nip}: {data}")
            result = data.get("result")
            subject = result.get("subject")
            status = subject.get("statusVat")
            return status == "Czynny"
        
        except requests.RequestException as e:
            print(f"API Connection Error: {e}")
            return False
        
    def send_history_via_email(self, email_address: str) -> bool:
        today_date = date.today().strftime("%Y-%m-%d")
        subject = "Account Transfer History " + today_date
        text = self.history_email_text_template.format(self.history)
        return SMTPClient.send(subject, text, email_address)