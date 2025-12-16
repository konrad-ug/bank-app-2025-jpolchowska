class Account:
    def __init__(self):
        self.balance = 0.0
        self.history = []

    def incoming_transfer(self, amount: float) -> bool:
        if amount > 0:
            self.balance += amount
            self.history.append(amount)
            return True
        return False

    def outgoing_transfer(self, amount: float) -> bool:
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.history.append(-amount)
            return True
        return False

    def express_transfer(self, amount: float, fee: float) -> bool:
        total = amount + fee
        if amount > 0 and self.balance - total >= -fee:
            self.balance -= total
            self.history.append(-amount)
            self.history.append(-fee)
            return True
        return False