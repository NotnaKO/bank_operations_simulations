from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from src.accounts.banks import DeclinedOperation
from .accounts import Account
from .money import Money


class Operation(ABC):
    @abstractmethod
    def make(self):
        """Make operation with account"""

    @abstractmethod
    def decline(self):
        """Decline operation with account"""


@dataclass
class Withdraw(Operation):
    _account: Account
    _summa: Money

    def make(self):
        self._account.withdraw(self._summa)

    def decline(self):
        self._account.put(self._summa)


@dataclass
class Put(Operation):
    _account: Account
    _summa: Money

    def make(self):
        self._account.put(self._summa)

    def decline(self):
        self._account.withdraw(self._summa)


@dataclass(init=False)
class Operator:
    operations: List[Operation]
    _account: Account | None
    _summa: Money | None

    def __init__(self):
        self.operations = []
        self._account = None
        self._summa = None

    def add_withdraw(self):
        self.operations.append(Withdraw(self._account, self._summa))

    def add_put(self):
        self.operations.append(Put(self._account, self._summa))

    def make_operations(self):
        for i, operation in enumerate(self.operations):
            try:
                operation.make()
            except DeclinedOperation:
                self.decline_operations(i)
                raise
        self.operations.clear()

    def decline_operations(self, end=None):
        if end is None:
            end = len(self.operations)
        for i in self.operations[:end][::-1]:
            i.decline()
        self.operations.clear()

    def make_withdraw(self, account: Account, summa: Money):
        self._account, self._summa = account, summa
        self.add_withdraw()
        self.make_operations()

    def make_put(self, account: Account, summa: Money):
        self._account, self._summa = account, summa
        self.add_put()
        self.make_operations()

    def make_transfer(self, account_1: Account, account_2: Account, summa: Money):
        self._account, self._summa = account_1, summa
        self.add_withdraw()
        self._account = account_2
        self.add_put()
        self.make_operations()
