"""Module with Checker class"""
from dataclasses import dataclass

from src.accounts import Money
from src.clients import Client
from src.data_adapter import DataAdapter, Singleton


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

    def approve_withdraw(self, bank_name: str, summa: Money):
        self._adapter.get_bank(bank_name).approve_withdraw(summa)
