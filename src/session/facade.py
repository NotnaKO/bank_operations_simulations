from dataclasses import dataclass
from logging import log, INFO

from src.accounts import ActionsCodes
from src.data_adapter import DataAdapter
from .assistants import AuthAssistant, \
    MainAssistant, AccountsAssistant, TransactionAssistant
from .io_implementation import IOImplementation, StandardConsoleIO


@dataclass
class SessionFacade:
    """Session moderator"""

    def __init__(self, adapter: DataAdapter, io: IOImplementation = StandardConsoleIO()):
        self._adapter: DataAdapter = adapter
        self._auth_assistant: AuthAssistant = AuthAssistant(io, adapter)
        self._main_assistant: MainAssistant = MainAssistant(io)
        self._account_assistant: AccountsAssistant = AccountsAssistant(io)
        self._transaction_assistant: TransactionAssistant = TransactionAssistant(io)

    def sign_up_or_sign_in(self):
        self._auth_assistant.print_choice()
        answer = self._auth_assistant.input()
        while answer not in ('1', '2'):
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
        log(INFO, "Sign up new client success")
        self.sign_in()

    def sign_in(self):
        log(INFO, "Starting sign in")
        answer = self._auth_assistant.login()
        if answer is None:
            self.sign_up_or_sign_in()
        else:
            log(INFO, "Sign in success")
            self._account_assistant.client = self._transaction_assistant.client \
                = self._adapter.get_client(answer[0], answer[1])
            self.main()

    def main(self):
        log(INFO, "Main part starts")
        while True:
            choice = self._main_assistant.print_choice()
            match choice:
                case ActionsCodes.SHOW_ACCOUNTS:
                    log(INFO, "Showing accounts of the client")
                    self._account_assistant.show_accounts()
                case ActionsCodes.CREATE_NEW_ACCOUNT:
                    log(INFO, "Creating new account")
                    account_type = self._account_assistant.choice_type_of_account()
                    account_creator = self._account_assistant.get_creator(account_type)
                    account = account_creator. \
                        create_account(self._account_assistant.get_money(),
                                       self._account_assistant.get_end_of_period(),
                                       self._account_assistant.get_bank(
                                           self._adapter.get_banks()).name)
                    log(INFO, f"Created {account}")
                    self._account_assistant.add_new_account(account)
                case ActionsCodes.MAKE_TRANSACTION:
                    transaction_type, account, summa = self._transaction_assistant.print_choice()
                    self._transaction_assistant.choice_operation(transaction_type, account, summa)
                    self._transaction_assistant.print_success()
                    log(INFO, "Transaction succeeded")
                case ActionsCodes.EXIT:
                    self._main_assistant.print_bye()
                    log(INFO, "End of the work with client")
                    return
