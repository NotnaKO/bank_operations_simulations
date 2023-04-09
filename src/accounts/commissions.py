from abc import abstractmethod
from dataclasses import dataclass

from src.serializable_base_class import SerializableByMyEncoder


class WrongSummaFormat(Exception):
    pass


def convert(summa: float) -> int:
    """convert float summa to int"""
    if not (summa * 100).is_integer():
        raise WrongSummaFormat
    return int(summa * 100)


class Commission(SerializableByMyEncoder):
    @abstractmethod
    def apply(self, summa: float) -> float:
        """Applying commission"""

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
