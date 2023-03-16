import sys
from dataclasses import dataclass
from logging import log, INFO, WARNING
from typing import TextIO

from source.python.assistants import SessionAssistant
from source.python.data_adapter import DataAdapter, UserNotExists, UserAlreadyExists


@dataclass
class SessionFacade:
    """Session moderator"""

    def __init__(self, _input: TextIO = sys.stdin,
                 _output: TextIO = sys.stdout):
        self._adapter: DataAdapter = DataAdapter()
        self._assistant: SessionAssistant = SessionAssistant(_input, _output)

    def sign_up_or_sign_in(self):
        self._assistant.print(
            """ Please, sign up or sign in(now and later choose the number to answer):
1)sign up
2)sign in""")
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
                new_client = self._assistant.generate_client()
            except AssertionError:
                self._assistant.print_try_again()
                log(WARNING, "Wrong user data in sign up")
            except UserAlreadyExists:
                self._assistant.print_try_again()
                log(WARNING, "Sign up to user already exist")
            else:
                success = True
                self._adapter.create_new_client(new_client)
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
                self._assistant.print("There are not users with such name and surname")
            else:
                success = True
            finally:
                if not success:
                    self.sign_up_or_sign_in()
                else:
                    log(INFO, "Sign in success")
                    self.main()

    def main(self):
        pass
