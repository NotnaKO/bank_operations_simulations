import json
from pathlib import Path
from typing import Type

from source.python.accounts.accounts import Account
from source.python.clients.client import Client


class UserNotExists(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class DataAlreadyLoaded(Exception):
    pass


class Encoder(json.JSONEncoder):
    def default(self, o: Client):
        if isinstance(o, Client) or isinstance(o, Account):
            return o.get_data()
        super().default(o)


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class DataAdapter(metaclass=Singleton):
    """Class to adapt work with data"""

    def __init__(self,
                 file_name: str | Path = Path(__file__).parents[2].joinpath("data/data.json")):
        self.file_name: Path | str = file_name
        self._data: dict | None = None
        with open(self.file_name) as f:
            self._data = json.load(f)
        self._file = open(self.file_name, "w")
        self.encoder: Type[json.JSONEncoder] = Encoder

    def __del__(self):
        json.dump(self._data, self._file,
                  cls=self.encoder)  # encoding Client to json object with Encoder
        self._file.close()

    def client_exists(self, name: str, surname: str) -> bool:
        """Check if client exists"""
        return f"{name} {surname}" in self._data["clients"]

    def create_new_client(self, new_client: Client) -> None:
        """Create new client by name and surname"""
        self._data["clients"][f"{new_client.name} {new_client.surname}"] = new_client

    def get_client(self, name: str, surname: str) -> Client:
        """Get client data"""
        if self.client_exists(name, surname):
            return self._data["clients"][f"{name} {surname}"]
        raise UserNotExists
