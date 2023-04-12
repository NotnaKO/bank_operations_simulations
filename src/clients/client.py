from dataclasses import dataclass
from typing import List, Type

from src.accounts import Account
from src.serializable_base_class import SerializableByMyEncoder
from .reliability import NotReliable, ReliabilityType, Reliable


@dataclass(init=False)
class Client(SerializableByMyEncoder):
    """Client class"""
    type: ReliabilityType
    accounts: List[Account]

    def __init__(self, name_and_surname: str, address: str | None, passport: str | None,
                 accounts: List[Account] | None = None):
        self._name, self._surname = name_and_surname.split()
        self._address = address
        self._passport = passport
        if accounts is None:
            self._accounts: List[Account] = []
        else:
            self._accounts = accounts

    @classmethod
    def from_data(cls, dictionary: dict):
        return cls(dictionary["name"] + ' ' + dictionary["surname"], dictionary["address"],
                   dictionary["passport"], dictionary["accounts"])

    @property
    def name_and_surname(self) -> str:
        return self._name + ' ' + self._surname

    @property
    def type(self) -> Type[NotReliable | Reliable]:
        if self._address is None or self._passport is None:
            return NotReliable
        return Reliable

    @property
    def information_to_add(self):
        answer: List[str] = []
        if self._address is None:
            answer.append("address")
        if self._passport is None:
            answer.append("passport")
        return ", ".join(answer[:-1]) + " and " + answer[-1]

    @property
    def accounts(self) -> List[Account]:
        return self._accounts

    def get_data(self) -> dict:
        return {"name": self._name, "surname": self._surname, "address": self._address,
                "passport": self._passport, "accounts": self.accounts, "__Client__": True}

    def add_account(self, acc: Account):
        self.accounts.append(acc)

    def have_accounts(self) -> bool:
        return bool(self.accounts)

    def complete(self, address: str, passport: str):
        if address:
            self._address = address
        if passport:
            self._passport = passport
