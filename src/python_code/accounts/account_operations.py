from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.python_code.accounts.accounts import Account


class Operation(ABC):
    @abstractmethod
    def make(self):
        pass


@dataclass
class Withdraw(Operation):
    _account: Account
    _summa: float

    def make(self):
        self._account.withdraw(self._summa)


@dataclass
class Put(Operation):
    _account: Account
    _summa: float

    def make(self):
        self._account.put(self._summa)


@dataclass(init=False)
class Operator:
    operations: list[Operation]
    _account: Account | None
    _summa: float | None

    def __init__(self):
        self.operations = []
        self._account = None
        self._summa = None

    def add_withdraw(self):
        self.operations.append(Withdraw(self._account, self._summa))

    def add_put(self):
        self.operations.append(Put(self._account, self._summa))

    def make_operations(self):
        for i in self.operations:
            i.make()
        self.operations.clear()

    def make_withdraw(self, account: Account, summa: float):
        self._account, self._summa = account, summa
        self.add_withdraw()
        self.make_operations()

    def make_put(self, account: Account, summa: float):
        self._account, self._summa = account, summa
        self.add_put()
        self.make_operations()

    def make_transfer(self, account_1: Account, account_2: Account, summa: float):
        self._account, self._summa = account_1, summa
        self.add_withdraw()
        self._account = account_2
        self.add_put()
        self.make_operations()
