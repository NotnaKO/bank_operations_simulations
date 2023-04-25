from dataclasses import dataclass
from typing import Union

from src.serializable_base_class import SerializableByMyEncoder


class WrongSummaFormat(Exception):
    pass


@dataclass(init=False)
class Money(SerializableByMyEncoder):
    """Class to work with money
    :raise ValueError in __init__ if summa could not be a float with 2 digits after point
    """
    _value: int

    def __init__(self, summa: Union["Money", int, float, str]):
        if isinstance(summa, Money):
            self._value = summa._value
        else:
            if isinstance(summa, str):
                summa = float(summa)
            self.value = summa

    @staticmethod
    def convert(summa: float) -> int:
        """convert float summa to int"""
        if not (summa * 100).is_integer():
            raise WrongSummaFormat
        return int(summa * 100)

    @property
    def value(self) -> float:
        return self._value / 100

    @value.setter
    def value(self, summa: float):
        self._value = self.convert(summa)

    @classmethod
    def __from_int(cls, value: int) -> "Money":
        return cls(round(value / 100, 2))

    def __lt__(self, other: Union["Money", int, float]):
        if isinstance(other, Money):
            return self._value < other._value
        if isinstance(other, int | float):
            return self._value < round(other * 100)
        raise NotImplementedError

    def __sub__(self, other: "Money"):
        if isinstance(other, Money):
            return self.__from_int(self._value - other._value)
        raise NotImplementedError

    def __add__(self, other: "Money"):
        if isinstance(other, Money):
            return self.__from_int(self._value + other._value)
        raise NotImplementedError

    def __mul__(self, other: float):
        if isinstance(other, float):
            return self.__from_int(round(self._value * other))
        raise NotImplementedError

    def __str__(self):
        return str(self.value)

    def get_data(self):
        return self.value
