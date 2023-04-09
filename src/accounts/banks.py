from dataclasses import dataclass

from src.serializable_base_class import SerializableByMyEncoder


@dataclass
class Bank(SerializableByMyEncoder):
    _bank_name: str

    @property
    def name(self):
        return self._bank_name

    @name.setter
    def name(self, val: str):
        self._bank_name = val

    def __str__(self):
        return self.name

    def get_data(self):
        return {"__Bank__": True, "name": self.name}
