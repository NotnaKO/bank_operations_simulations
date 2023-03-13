from dataclasses import dataclass
from typing import Type

from source.python.clients.reliability import NotReliable, Reliable


@dataclass
class Client:
    _name: str
    _surname: str
    _address: str | None = None
    _passport: str | None = None

    @property
    def name(self):
        return self._name

    @property
    def surname(self):
        return self._surname

    @property
    def address(self):
        return self._address

    @property
    def passport(self):
        return self._passport  # Todo: is it ok?

    @property
    def type(self) -> Type[NotReliable | Reliable]:
        if self.address is None or self.passport is None:
            return NotReliable
        return Reliable
