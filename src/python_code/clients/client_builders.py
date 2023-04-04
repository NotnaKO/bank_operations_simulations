from abc import ABC, abstractmethod

from src.python_code.clients.client import Client


class ClientBuilder(ABC):

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def set_name_and_surname(self, content: list):
        """Set name and surname for the client"""
        pass

    @abstractmethod
    def set_address(self, content: list):
        """Set address for the client"""
        pass

    @abstractmethod
    def set_passport(self, content: list):
        """Set passport for the client"""
        pass

    @abstractmethod
    def build(self, content: list) -> Client:
        pass


class BaseClientBuilder(ClientBuilder):
    """Client only with name and surname"""

    def __init__(self):
        self.content = []

    def reset(self):
        self.content = []

    def set_name_and_surname(self, content: list):
        self.content.extend((content[0], content[1]))

    def set_address(self, content: list):
        self.content.append(None)

    def set_passport(self, content: list):
        self.content.append(None)

    def build(self, content: list) -> Client:
        self.reset()
        self.set_name_and_surname(content)
        self.set_address(content)
        self.set_passport(content)
        return Client(*self.content)


class ClientWithAddressBuilder(BaseClientBuilder):
    """Client with name, surname and address"""

    def set_address(self, content: list):
        self.content.append(content[2])


class ClientWithPassportBuilder(BaseClientBuilder):
    """Client with name, surname and passport"""

    def set_passport(self, content: list):
        self.content.append(content[2])


class FullClientBuilder(ClientWithAddressBuilder):
    """Client with name, surname, address and passport"""

    def set_passport(self, content: list):
        self.content.append(content[3])
