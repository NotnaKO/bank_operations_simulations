from abc import abstractmethod
from dataclasses import dataclass
from datetime import date, datetime

from src.accounts.banks import DeclinedOperation
from src.serializable_base_class import SerializableByMyEncoder
from .commissions import Commission
from .money import Money


class InsufficientFunds(DeclinedOperation):
    """Exception when insufficient funds in withdraw"""


class WithdrawBeforeEnd(DeclinedOperation):
    """Exception when user trying to withdraw funds before the end of the deposit"""


class Account(SerializableByMyEncoder):
    """Accounts base class"""

    def __init__(self, begin_balance: float, end, bank_name: str):
        """Taking money with float but convert it to int"""
        self.balance = begin_balance
        self._end = end
        self._bank_name = bank_name

    @property
    def balance(self) -> Money:
        """Get balance of the account"""
        return self._balance

    @balance.setter
    def balance(self, summa: float):
        self._balance = Money(summa)

    @property
    def end(self) -> date:
        return self._end

    @property
    def bank_name(self):
        return self._bank_name

    @bank_name.setter
    def bank_name(self, val: str):
        self._bank_name = val

    @abstractmethod
    def withdraw(self, summa: Money):
        raise NotImplementedError

    @abstractmethod
    def put(self, summa: Money):
        raise NotImplementedError

    def get_data(self) -> dict:
        raise NotImplementedError


@dataclass(init=False)
class Debit(Account):
    def withdraw(self, summa: Money):
        if summa > self.balance:
            raise InsufficientFunds(
                f"""You have tried to withdraw too much.
You have: {self.balance}. You ask for: {summa}""")
        self.balance -= summa

    def put(self, summa: Money):
        self.balance += summa

    def get_data(self) -> dict:
        return {"type": "Debit", "balance": self.balance, "end": self.end, "__Account__": True,
                "bank_name": self.bank_name}

    def __str__(self):
        return f"Debit from {self.bank_name} with balance {self.balance}" + \
            f" and end {self.end.strftime('%d.%m.%Y')}"


@dataclass(init=False)
class Deposit(Account):
    def withdraw(self, summa: Money):
        if datetime.today() < self.end:
            raise WithdrawBeforeEnd(f"""You have tried to withdraw too early.
End of this deposit is {self.end.strftime("%d.%m.%Y")}.
Today: {datetime.today().strftime("%d.%m.%Y")}""")
        if summa > self.balance:
            raise InsufficientFunds(
                f"""You have tried to withdraw too much.
You have: {self.balance}. You ask for: {summa}""")
        self.balance -= summa

    def put(self, summa: Money):
        self.balance += summa

    def get_data(self) -> dict:
        return {"type": "Deposit", "balance": self.balance, "end": self.end, "__Account__": True,
                "bank_name": self.bank_name}

    def __str__(self):
        return f"Deposit from {self.bank_name} with balance {self.balance}" + \
            f" and end {self.end.strftime('%d.%m.%Y')}"


@dataclass(init=False)
class Credit(Account):
    def __init__(self, begin_balance: float, end: date, commission: Commission, bank_name: str):
        self._commission: Commission = commission
        super().__init__(begin_balance, end, bank_name)

    @property
    def commission(self) -> Commission:
        return self._commission

    def withdraw(self, summa: Money):
        if self.balance < 0:
            summa = self.commission.apply(summa)
        self.balance -= summa

    def put(self, summa: Money):
        self.balance += summa

    def get_data(self) -> dict:
        return {"type": "Credit", "balance": self.balance, "end": self.end,
                "commission": self.commission.get_data(), "__Account__": True,
                "bank_name": self.bank_name}

    def __str__(self):
        ans = f"Credit from {self.bank_name} with balance {self.balance}," + \
              f" end {self.end.strftime('%d.%m.%Y')} and {self.commission}"
        return ans
