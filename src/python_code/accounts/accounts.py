from dataclasses import dataclass
from datetime import date, datetime

from src.python_code.accounts.commissions import convert, Commission
from src.python_code.data.serializable_base_class import SerializableByMyEncoder


class InsufficientFunds(Exception):
    pass


class WithdrawBeforeEnd(Exception):
    pass


class Account(SerializableByMyEncoder):
    """Accounts base class"""

    def __init__(self, begin_balance: float, end, bank_name: str):
        """Taking money with float but convert it to int"""
        self.balance = begin_balance
        self._end = end
        self._bank_name = bank_name

    @property
    def balance(self) -> float:
        """Get balance of the account"""
        return self._balance / 100

    @balance.setter
    def balance(self, summa: float):
        self._balance = convert(summa)

    @property
    def end(self) -> date:
        return self._end

    @property
    def bank_name(self):
        return self._bank_name

    @bank_name.setter
    def bank_name(self, val: str):
        self._bank_name = val

    def withdraw(self, summa: float):
        raise NotImplementedError

    def put(self, summa: float):
        raise NotImplementedError

    def get_data(self) -> dict:
        raise NotImplementedError


@dataclass(init=False)
class Debit(Account):
    def withdraw(self, summa: float):
        if summa > self.balance:
            raise InsufficientFunds
        self.balance = round(self.balance - summa, 2)

    def put(self, summa: float):
        self.balance = round(self.balance + summa, 2)

    def get_data(self) -> dict:
        return {"type": "Debit", "balance": self.balance, "end": self.end, "__Account__": True,
                "bank_name": self.bank_name}

    def __str__(self):
        return f"Debit from {self.bank_name} with balance {self.balance}" + \
            f" and end {self.end.strftime('%d.%m.%Y')}"


@dataclass(init=False)
class Deposit(Account):
    def withdraw(self, summa: float):
        if datetime.today() < self.end:
            raise WithdrawBeforeEnd
        if summa > self.balance:
            raise InsufficientFunds
        self.balance = round(self.balance - summa, 2)

    def put(self, summa: float):
        self.balance = round(self.balance + summa, 2)

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

    def withdraw(self, summa: float):
        if self.balance < 0:
            summa = self.commission.apply(summa)
        self.balance = round(self.balance - summa, 2)

    def put(self, summa: float):
        self.balance = round(self.balance + summa, 2)

    def get_data(self) -> dict:
        return {"type": "Credit", "balance": self.balance, "end": self.end,
                "commission": self.commission.get_data(), "__Account__": True,
                "bank_name": self.bank_name}

    def __str__(self):
        ans = f"Credit from {self.bank_name} with balance {self.balance}," + \
              f" end {self.end.strftime('%d.%m.%Y')} and {self.commission}"
        return ans
