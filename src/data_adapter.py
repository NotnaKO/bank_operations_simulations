"""Module with Data Adapter class and errors with users"""

import datetime
import json
from dataclasses import dataclass
from logging import INFO, log
from pathlib import Path

from src.accounts import Account, Commission, Credit, Debit, Deposit, FixedCommission, \
    PercentCommission
from src.accounts.banks import Bank
from src.clients import Client
from src.project_data import ProjectData
from src.serializable_base_class import SerializableByMyEncoder


class UserNotExists(Exception):
    """Exception when user does not exist in data"""


class UserAlreadyExists(Exception):
    """Exception when user already exist"""


class DataAlreadyLoaded(Exception):
    """Exception when attempt to load data twice"""


class Encoder(json.JSONEncoder):
    """Encoder to my objects"""

    def default(self, o):
        if isinstance(o, SerializableByMyEncoder):
            return o.get_data()
        if isinstance(o, datetime.date):
            return {"value": o.strftime("%d.%m.%Y"), "__date__": True}
        return super().default(o)


class Decoder(json.JSONDecoder):
    """Decoder to my objects"""

    @staticmethod
    def choose_account(dictionary: dict) -> Account:
        match dictionary["type"]:
            case "Debit":
                return Debit(dictionary["balance"], dictionary["end"], dictionary["bank_name"])
            case "Deposit":
                return Deposit(dictionary["balance"], dictionary["end"],
                               dictionary["bank_name"])
            case "Credit":
                return Credit(dictionary["balance"], dictionary["end"],
                              dictionary["commission"], dictionary["bank_name"])
        raise RuntimeError

    @staticmethod
    def choose_commission(dictionary: dict) -> Commission:
        match dictionary["type"]:
            case "percent":
                return PercentCommission(dictionary["value"])
            case "fixed":
                return FixedCommission(dictionary["value"])
        raise RuntimeError

    @staticmethod
    def loading_function(dictionary: dict):
        """function to load my function from json"""
        if "__Client__" in dictionary:
            return Client.from_data(dictionary)
        if "__date__" in dictionary:
            return datetime.datetime.strptime(dictionary["value"], "%d.%m.%Y")
        if "__Account__" in dictionary:
            return Decoder.choose_account(dictionary)
        if "__Commission__" in dictionary:
            return Decoder.choose_commission(dictionary)
        if "__Bank__" in dictionary:
            return Bank(dictionary["name"], dictionary["bound"])
        return dictionary

    def __init__(self, *args, **kwargs):
        kwargs["object_hook"] = self.loading_function
        super().__init__(*args, **kwargs)


class Singleton(type):
    """Singleton metaclass to creates singletons"""
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        elif isinstance(cls, DataAdapter):
            raise DataAlreadyLoaded
        return cls._instance


class BankNotExists(Exception):
    """Exception when bank does not exist"""


@dataclass(init=False)
class DataAdapter(metaclass=Singleton):
    """Class to adapt work with data"""

    def __init__(self,
                 file_name: str | Path = ProjectData.data_path()):
        self.file_name: Path | str = file_name
        self._data: dict | None = None

    def __enter__(self):
        with open(self.file_name, encoding="utf-8") as file:
            self._data = json.load(file, cls=Decoder)
        log(INFO, "Data loaded")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(self._data, file, indent=2, sort_keys=True,
                      cls=Encoder)  # encoding Client to json object with Encoder
        log(INFO, "Data saved")
        if exc_val:
            raise

    def bank_exists(self, name: str) -> bool:
        return name in self._data["banks"]

    def create_new_client(self, new_client: Client) -> None:
        """Create new client by name and surname"""
        if new_client.name_and_surname in self._data["clients"]:
            raise UserAlreadyExists
        self._data["clients"][new_client.name_and_surname] = new_client

    def get_client(self, name_and_surname: str) -> Client:
        """Get client data"""
        try:
            return self._data["clients"][name_and_surname]
        except KeyError as exc:
            raise UserNotExists from exc

    def get_banks(self):
        return self._data["banks"]

    def get_bank(self, name: str) -> Bank:
        """Get bank data"""
        if self.bank_exists(name):
            return self._data["banks"][name]
        raise BankNotExists
