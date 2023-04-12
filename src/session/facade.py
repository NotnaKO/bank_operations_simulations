from dataclasses import dataclass
from logging import INFO, log

from src.data_adapter import DataAdapter
from .assistants import AccountsAssistant, AuthAssistant, LoginFail, MainAssistant, \
    TransactionAssistant
from .codes_to_answers import ActionsCodes
from .io_implementation import IOImplementation, StandardConsoleIO


@dataclass
class SessionFacade:
    """Session moderator"""

    def __init__(self, adapter: DataAdapter,
                 input_and_output: IOImplementation = StandardConsoleIO()):
        self._adapter: DataAdapter = adapter
        self._auth_assistant: AuthAssistant = AuthAssistant(input_and_output, adapter)
        self._main_assistant: MainAssistant = MainAssistant(input_and_output)
        self._account_assistant: AccountsAssistant = AccountsAssistant(input_and_output)
        self._transaction_assistant: TransactionAssistant = TransactionAssistant(input_and_output,
                                                                                 adapter)

    def sign_up_or_sign_in(self):
        match self._auth_assistant.sign_in_or_sign_up():
            case ActionsCodes.SIGN_UP:
                self.sign_up()
            case ActionsCodes.SIGN_IN:
                self.sign_in()
            case _:
                raise RuntimeError

    def start_session(self):
        log(INFO, "Starting session")
        self._auth_assistant.print_welcome()
        self.sign_up_or_sign_in()

    def sign_up(self):
        log(INFO, "Starting sign up")
        self._adapter.create_new_client(self._auth_assistant.sign_up())
        log(INFO, "Sign up new client success")
        self.sign_in()

    def set_client(self, name_and_surname: str):
        self._account_assistant.client = self._transaction_assistant.client = \
            self._main_assistant.client = self._adapter.get_client(name_and_surname)

    def sign_in(self):
        log(INFO, "Starting sign in")
        try:
            answer = self._auth_assistant.login()
        except LoginFail:
            self.sign_up_or_sign_in()
        else:
            log(INFO, "Sign in success")
            self.set_client(answer)
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
                case ActionsCodes.EXIT:
                    self._main_assistant.print_bye()
                    log(INFO, "End of the work with client")
                    return
                case ActionsCodes.COMPLETE_INFORMATION:
                    self._auth_assistant.complete_information(self._main_assistant.client)
                case _:
                    raise RuntimeError
