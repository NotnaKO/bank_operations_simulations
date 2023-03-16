import datetime
from dataclasses import dataclass
from typing import AnyStr, TextIO

from source.python.accounts.accounts import Commission, WrongSummaFormat
from source.python.checker_and_exceptions import Checker
from source.python.clients.client import Client
from source.python.clients.client_builders import BaseClientBuilder, FullClientBuilder, \
    ClientWithAddressBuilder, ClientWithPassportBuilder
from source.python.data_adapter import UserNotExists, UserAlreadyExists


@dataclass
class IOAssistant:
    _input: TextIO
    _output: TextIO

    def print(self, *args: AnyStr):
        """Print lines in the output"""
        print(*args, file=self._output)

    def input(self) -> AnyStr:
        """Read one line from the input"""
        return self._input.readline().rstrip()


@dataclass
class SessionAssistant(IOAssistant):
    """Class helping with input and output"""

    _user_data: list = None
    _with_passport: bool = None

    def print_welcome(self):
        self.print("""\t\t\t\tWelcome to the bank system!\t\t\t\t""")

    def print_try_again(self):
        self.print("Error, please check your answer and try again.")

    def learn_about_user(self):
        self.print("Let's try to sign up:\nEnter your name and surname separated by a space:")
        name, surname = self.input().split()
        self.print("Enter your address(optional, press Enter to continue without address)")
        address = self.input()
        self.print("Enter your passport(optional, press Enter to continue without passport)")
        passport = self.input()
        self._user_data = list(filter(lambda x: x, (name, surname, address, passport)))
        self._with_passport = bool(passport)

    def generate_client(self):
        assert self._user_data and len(self._user_data) >= 2
        match len(self._user_data):
            case 2:
                builder = BaseClientBuilder()
            case 4:
                builder = FullClientBuilder()
            case _:
                if not self._with_passport:
                    builder = ClientWithAddressBuilder()
                else:
                    builder = ClientWithPassportBuilder()
        new_client: Client = builder.build(self._user_data)
        try:
            Checker.check_if_user_exists(new_client.name, new_client.surname)
        except UserNotExists:
            return new_client
        else:
            raise UserAlreadyExists

    def login(self):
        self.print("Enter your name and surname:")  # Todo: пароль?

        answer = self.input().split()
        assert len(answer) == 2
        Checker.check_if_user_exists(*answer)


class AccountsAssistant(IOAssistant):
    def get_money(self) -> float:
        success = False
        money = None
        while not success:
            self.print("Enter the summa for begin:")
            try:
                money = float(self.input())
                if not (money * 100).is_integer():
                    raise WrongSummaFormat
            except ValueError:
                self.print("Your summ should be integer or float")
            except WrongSummaFormat:
                self.print("Your summa should have equal or less than 2 numbers after point")
            else:
                success = True
        return money

    def get_end_of_period(self) -> datetime.date:
        pass

    def get_commission(self) -> Commission:
        pass
