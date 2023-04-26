from dataclasses import dataclass

from src.accounts.money import Money
from src.serializable_base_class import SerializableByMyEncoder


@dataclass(init=False)
class Bank(SerializableByMyEncoder):
    _bank_name: str
    _withdraw_bound: Money

    def __init__(self, name: str, bound: float):
        self._bank_name = name
        self._withdraw_bound = Money(bound)

    @property
    def name(self):
        return self._bank_name

    @name.setter
    def name(self, val: str):
        self._bank_name = val

    def approve_withdraw(self, summa: Money):
        if summa > self._withdraw_bound:
            raise DeclinedOperation(f"""
You have incomplete information. That's why you have a bound 
{self._withdraw_bound} by this account.(You want to withdraw {summa}).""".lstrip())

    def __str__(self):
        return self.name

    def get_data(self):
        return {"__Bank__": True, "name": self.name, "bound": self._withdraw_bound.value}


class DeclinedOperation(Exception):
    """Exception when operation is declined"""
