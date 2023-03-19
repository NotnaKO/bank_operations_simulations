import datetime
import json
from dataclasses import dataclass
from logging import log, INFO
from pathlib import Path

from src.python_code.accounts.accounts import Debit, Deposit, Credit, FixedCommission, \
    PercentCommission
from src.python_code.accounts.banks import Bank
from src.python_code.clients.client import Client
from src.python_code.data.serializable_base_class import SerializableByMyEncoder


class UserNotExists(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class DataAlreadyLoaded(Exception):
    pass


class Encoder(json.JSONEncoder):
    def default(self, o: Client):
        if isinstance(o, SerializableByMyEncoder):
            return o.get_data()
        if isinstance(o, datetime.date):
            return {"value": o.strftime("%d.%m.%Y"), "__date__": True}
        super().default(o)


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            raise DataAlreadyLoaded
        return cls._instance


@dataclass(init=False)
class DataAdapter(metaclass=Singleton):
    """Class to adapt work with data"""

    @staticmethod
    def loading_function(d: dict):
        if "__Client__" in d:
            return Client(d["name"], d["surname"], d["address"], d["passport"], d["accounts"])
        if "__date__" in d:
            return datetime.datetime.strptime(d["value"], "%d.%m.%Y")
        if "__Account__" in d:
            match d["type"]:
                case "Debit":
                    return Debit(d["balance"], d["end"], d["bank_name"])
                case "Deposit":
                    return Deposit(d["balance"], d["end"], d["bank_name"])
                case "Credit":
                    return Credit(d["balance"], d["end"], d["commission"], d["bank_name"])
        if "__Commission__" in d:
            match d["type"]:
                case "percent":
                    return PercentCommission(d["value"])
                case "fixed":
                    return FixedCommission(d["value"])
        if "__Bank__" in d:
            return Bank(d["name"])
        return d

    def __init__(self,
                 file_name: str | Path = Path(__file__).parents[3].joinpath("data/data.json")):
        self.file_name: Path | str = file_name
        self._data: dict | None = None

    def __enter__(self):
        with open(self.file_name) as f:
            self._data = json.load(f, object_hook=self.loading_function)
        log(INFO, "Data loaded")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.file_name, "w") as file:
            json.dump(self._data, file, indent=2, sort_keys=True,
                      cls=Encoder)  # encoding Client to json object with Encoder
        log(INFO, "Data saved")
        if exc_val:
            raise

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

    def get_banks(self):
        return self._data["banks"]
