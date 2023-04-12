from abc import abstractmethod
from dataclasses import dataclass

from src.serializable_base_class import SerializableByMyEncoder
from .money import Money


class Commission(SerializableByMyEncoder):
    @abstractmethod
    def apply(self, summa: Money) -> Money:
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

    def apply(self, summa: Money) -> Money:
        return summa * self.percent

    def get_data(self):
        return {"type": "percent", "value": self.percent, "__Commission__": True}

    def __str__(self):
        return f"commission with percent {self.percent}"


@dataclass(init=False)
class FixedCommission(Commission):
    def __init__(self, commission: Money):
        self.commission: Money = commission

    def apply(self, summa: Money) -> float:
        return summa - self.commission

    def get_data(self):
        return {"type": "fixed", "value": self.commission, "__Commission__": True}

    def __str__(self):
        return f"fixed commission {self.commission}"
