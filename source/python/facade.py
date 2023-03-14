import sys
from dataclasses import dataclass
from logging import log, INFO, WARNING
from typing import TextIO, AnyStr

from source.python.checker_and_exceptions import Checker, UserNotExists, UserAlreadyExists
from source.python.clients.client import Client
from source.python.clients.client_builders import BaseClientBuilder, FullClientBuilder, \
    ClientWithAddressBuilder, ClientWithPassportBuilder


@dataclass
class Assistant:
    """Class helping with input and output"""
    _input: TextIO
    _output: TextIO
    _user_data: list = None
    _with_passport: bool = None

    def print(self, *args: AnyStr):
        """Print lines in the output"""
        self._output.writelines(args)

    def input(self) -> AnyStr:
        """Read one line from the input"""
        return self._input.readline().rstrip()

    def print_welcome(self):
        self.print("""\t\t\t\tWelcome to the bank system!\t\t\t\t""")

    def print_try_again(self):
        self.print("Error, please check your answer and try again.\n")

    def learn_about_user(self):
        pass

    def generate_user(self):
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
            pass
            # Todo: запись клиента
        else:
            raise UserAlreadyExists

    def login(self):
        self.print("Введите свою имя и фамилию в строчку через пробел:\n")  # Todo: пароль?

        answer = self.input().split()
        assert len(answer) == 2
        Checker.check_if_user_exists(*answer)


@dataclass
class SessionFacade:
    """Session moderator"""

    def __init__(self, _input: TextIO = sys.stdin, _output: TextIO = sys.stdout):
        self._assistant = Assistant(_input, _output)

    def sign_up_or_sign_in(self):
        self._assistant.print(
            """ Please, sign up or sign in(now and later choose the number to answer):
1)sign up
2)sign in\n""")
        answer = self._assistant.input()
        while answer != '1' and answer != '2':
            self._assistant.print_try_again()
            answer = self._assistant.input()

        if answer == '1':
            self.sign_up()
        elif answer == '2':
            self.sign_in()

    def start_session(self):
        log(INFO, "Starting session")
        self._assistant.print_welcome()
        self.sign_up_or_sign_in()

    def sign_up(self):
        log(INFO, "Starting sign up")
        success = False
        while not success:
            self._assistant.learn_about_user()
            try:
                self._assistant.generate_user()
            except AssertionError:
                self._assistant.print_try_again()
                log(WARNING, "Wrong user data in sign up")
            except UserAlreadyExists:
                self._assistant.print_try_again()
                log(WARNING, "Sign up to user already exist")
            else:
                success = True
        self._assistant.print("Sign up succeeded")
        log(INFO, "Sign up new user success")
        self.sign_in()

    def sign_in(self):
        log(INFO, "Starting sign in")
        success = False
        while not success:
            try:
                self._assistant.login()
            except AssertionError:
                self._assistant.print("You name and surname should be only two words")
            except UserNotExists:
                self._assistant.print("There are not users with such ")
            else:
                success = True
            finally:
                if not success:
                    self.sign_up_or_sign_in()
                else:
                    self.main()

    def main(self):
        pass
