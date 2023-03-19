from dataclasses import dataclass

from source.python.data.data_adapter import DataAdapter


@dataclass
class Checker:
    _adapter: DataAdapter

    def check_if_user_exists(self, name: str, surname: str):
        self._adapter.get_client(name, surname)
