from abc import ABC, abstractmethod

from source.python.clients.client import Client
from source.python.facade import SessionFacade


class ClientBuilder(ABC):

    @abstractmethod
    def set_name_and_surname(self, name: str, surname: str):
        """Set name and surname for the client"""
        pass

    @abstractmethod
    def set_address(self, address: str | None):
        """Set address for the client"""
        pass

    @abstractmethod
    def set_passport(self, passport: str | None):
        """Set password for the client"""
        pass

    @abstractmethod
    def build(self, session: SessionFacade) -> Client:
        pass


class BaseClientBuilder(ClientBuilder):
    """Client only with name and surname"""

    def __init__(self):
        self.content = []

    def set_name_and_surname(self, name: str, surname: str):
        self.content.extend((name, surname))

    def set_address(self, address: str | None = None):
        self.content.append(None)

    def set_passport(self, passport: str | None = None):
        self.content.append(None)

    def build(self, session: SessionFacade) -> Client:
        session.get_client_data(self)
        return Client(*self.content)


class ClientWithAddressBuilder(BaseClientBuilder):
    """Client with name, surname and address"""

    def set_address(self, address: str | None = None):
        self.content.append(address)


class ClientWithPassportBuilder(BaseClientBuilder):
    """Client with name, surname and passport"""

    def set_passport(self, passport: str | None = None):
        self.content.append(passport)


class FullClientBuilder(ClientWithAddressBuilder):
    """Client with name, surname, address and passport"""

    def set_passport(self, passport: str | None = None):
        self.content.append(passport)
