class Account:
    def __init__(self):
        self.balance = 0.0

    def incoming_transfer(self, amount: float) -> None:
        if amount > 0:
            self.balance += amount

    def outgoing_transfer(self, amount: float) -> None:
        if amount > 0 and amount <= self.balance:
            self.balance -= amount

    def express_transfer(self, amount: float, fee: float) -> None:
        total = amount + fee
        if amount > 0 and self.balance - total >= -fee:
            self.balance -= total