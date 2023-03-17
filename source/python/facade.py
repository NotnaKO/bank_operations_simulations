import sys
from dataclasses import dataclass
from logging import log, INFO
from typing import TextIO

from source.python.accounts.accounts_factory import DebitCreator, DepositCreator, CreditCreator
from source.python.assistants import AuthAssistant, MainAssistant, AccountsAssistant
from source.python.data_adapter import DataAdapter


@dataclass
class SessionFacade:
    """Session moderator"""

    def __init__(self, _input: TextIO = sys.stdin,
                 _output: TextIO = sys.stdout):
        self._adapter: DataAdapter = DataAdapter()
        self._auth_assistant: AuthAssistant = AuthAssistant(_input, _output)
        self._main_assistant: MainAssistant = MainAssistant(_input, _output)
        self._account_assistant: AccountsAssistant = AccountsAssistant(_input, _output)

    def sign_up_or_sign_in(self):
        self._auth_assistant.print_choice()
        answer = self._auth_assistant.input()
        while answer != '1' and answer != '2':
            self._auth_assistant.print_try_again()
            answer = self._auth_assistant.input()

        if answer == '1':
            self.sign_up()
        elif answer == '2':
            self.sign_in()

    def start_session(self):
        log(INFO, "Starting session")
        self._auth_assistant.print_welcome()
        self.sign_up_or_sign_in()

    def sign_up(self):
        log(INFO, "Starting sign up")
        self._adapter.create_new_client(self._auth_assistant.sign_up())
        log(INFO, "Sign up new user success")
        self.sign_in()

    def sign_in(self):
        log(INFO, "Starting sign in")
        answer = self._auth_assistant.login()
        if answer is None:
            self.sign_up_or_sign_in()
        else:
            log(INFO, "Sign in success")
            self._main_assistant.client = self._adapter.get_client(answer[0], answer[1])
            self.main()

    def main(self):
        log(INFO, "Main part starts")
        choice = self._main_assistant.print_choice()
        if choice == 1:
            log(INFO, "Showing accounts of the client")
            self._main_assistant.show_accounts()
        else:
            log(INFO, "Creating new account")
            account_type = self._main_assistant.choice_type_of_account()
            account_creator = None
            match account_type:
                case 1:
                    account_creator = DebitCreator(self._account_assistant)
                case 2:
                    account_creator = DepositCreator(self._account_assistant)
                case 3:
                    account_creator = CreditCreator(self._account_assistant)
            assert account_creator is not None
            account = account_creator.create_account()
            log(INFO, f"Created {account}")
            self._main_assistant.add_new_account(account)
