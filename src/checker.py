"""Module with Checker class"""
from dataclasses import dataclass

from src.accounts import Account, Money
from src.clients import Client, NotReliable
from src.data_adapter import DataAdapter, Singleton


class InvalidTransfer(Exception):
    pass


@dataclass
class Checker(metaclass=Singleton):
    """Class to check user in data"""
    _adapter: DataAdapter

    def check_if_client_exists_by_name(self, name: str, surname: str):
        """Check if client exists in data by name and surname"""
        self._adapter.get_client(f"{name} {surname}")

    def check_if_client_exists_by_client(self, client: Client):
        """Check if user exists in data"""
        self._adapter.get_client(client.name_and_surname)

    def approve_withdraw(self, client: Client, account: Account, summa: Money):
        if client.type is NotReliable:
            self._adapter.get_bank(account.bank_name).approve_withdraw(summa)

    def approve_transfer(self, client: Client, account: Account, second_account: Account,
                         summa: Money):
        self.approve_withdraw(client, account, summa)
        if account is second_account:
            raise InvalidTransfer("You want to transfer money to the same account")
