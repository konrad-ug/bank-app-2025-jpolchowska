from src.personal_account import PersonalAccount
from typing import List

class AccountsRegistry:
    def __init__(self):
        self.accounts: List[PersonalAccount] = []

    def add_account(self, account: PersonalAccount):
        if self.get_account_by_pesel(account.pesel):
            return False
        self.accounts.append(account)
        return True

    def get_account_by_pesel(self, pesel):
        for account in self.accounts:
            if account.pesel == pesel:
                return account
        return None

    def get_all_accounts(self):
        return self.accounts

    def get_account_count(self):
        return len(self.accounts)

    def delete_account(self, pesel):
        account = self.get_account_by_pesel(pesel)
        if account is not None:
            self.accounts.remove(account)