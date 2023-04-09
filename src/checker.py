"""Module with Checker class"""
from dataclasses import dataclass

from src.data_adapter import DataAdapter


@dataclass
class Checker:
    """Class to check user in data"""
    _adapter: DataAdapter

    def check_if_user_exists(self, name: str, surname: str):
        """Check if user exists in data"""
        self._adapter.get_client(name, surname)
