from abc import ABC, abstractmethod

class AccountsRepository(ABC):

    @abstractmethod
    def save_all(self, accounts: list):
        # pass
        raise NotImplementedError("save_all must be implemented")

    @abstractmethod
    def load_all(self) -> list:
        # pass
        raise NotImplementedError("load_all must be implemented")