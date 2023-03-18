from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime


class WrongSummaFormat(Exception):
    pass


class InsufficientFunds(Exception):
    pass


class WithdrawBeforeEnd(Exception):
    pass


def convert(summa: float) -> int:
    """convert float summa to int"""
    if not (summa * 100).is_integer():
        raise WrongSummaFormat
    return int(summa * 100)


class Commission(ABC):
    @abstractmethod
    def apply(self, summa: float) -> float:
        """Applying commission"""
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


@dataclass
class PercentCommission(Commission):
    percent: float

    def apply(self, summa: float) -> float:
        summa = convert(summa)
        summa *= self.percent
        return round(summa / 100, 2)

    def get_data(self):
        return {"type": "percent", "value": self.percent, "__Commission__": True}

    def __str__(self):
        return f"commission with percent {self.percent}"


@dataclass(init=False)
class FixedCommission(Commission):
    def __init__(self, commission: float):
        self.commission: int = convert(commission)

    def apply(self, summa: float) -> float:
        return convert(summa) - self.commission

    def get_data(self):
        return {"type": "fixed", "value": self.commission, "__Commission__": True}

    def __str__(self):
        return f"fixed commission {self.commission}"


class Account:
    """Accounts base class(not pure abstract)"""

    def __init__(self, begin_balance: float, end):
        """Taking money with float but convert it to int"""
        self.balance = begin_balance
        self._end = end

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

    @abstractmethod
    def withdraw(self, summa: float):
        pass

    @abstractmethod
    def put(self, summa: float):
        pass

    @abstractmethod
    def get_data(self) -> dict:
        pass

    @abstractmethod
    def __str__(self):
        pass


class Debit(Account):
    def withdraw(self, summa: float):
        if summa > self.balance:
            raise InsufficientFunds
        self.balance = round(self.balance - summa, 2)

    def put(self, summa: float):
        self.balance = round(self.balance + summa, 2)

    def get_data(self) -> dict:
        return {"type": "Debit", "balance": self.balance, "end": self.end, "__Account__": True}

    def __str__(self):
        return f"Debit with balance {self.balance} and end {self.end.strftime('%d.%m.%Y')}"


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
        return {"type": "Deposit", "balance": self.balance, "end": self.end, "__Account__": True}

    def __str__(self):
        return f"Deposit with balance {self.balance} and end {self.end.strftime('%d.%m.%Y')}"


class Credit(Account):
    def __init__(self, begin_balance: float, end: date, commission: Commission):
        self._commission: Commission = commission
        super().__init__(begin_balance, end)

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
                "commission": self.commission.get_data(), "__Account__": True}

    def __str__(self):
        ans = f"Credit with balance {self.balance}," + \
              f" end {self.end.strftime('%d.%m.%Y')} and {self.commission}"
        return ans
