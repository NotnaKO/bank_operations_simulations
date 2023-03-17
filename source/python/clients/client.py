from dataclasses import dataclass
from typing import Type

from source.python.accounts.accounts import Account
from source.python.clients.reliability import NotReliable, Reliable, ReliabilityType


@dataclass(init=False)
class Client:
    type: ReliabilityType
    accounts: list[Account]

    def __init__(self, name: str, surname: str, address: str, passport: str):
        self._name = name
        self._surname = surname
        self._address = address
        self._passport = passport
        self._accounts = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def surname(self) -> str:
        return self._surname

    @property
    def address(self) -> str:
        return self._address

    @property
    def passport(self) -> str:
        return self._passport  # Todo: is it ok?

    @property
    def type(self) -> Type[NotReliable | Reliable]:
        if self.address is None or self.passport is None:
            return NotReliable
        return Reliable

    @property
    def accounts(self) -> list[Account]:
        return self._accounts

    def get_data(self) -> dict:
        return {"name": self.name, "surname": self.surname, "address": self.address,
                "passport": self.passport, "accounts": self.accounts}

    def add_account(self, acc: Account):
        self.accounts.append(acc)

    def have_accounts(self) -> bool:
        return bool(self.accounts)
