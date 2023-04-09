import datetime
from dataclasses import dataclass
from logging import log, WARNING

from src.accounts import Operator, WrongSummaFormat, Bank, AccountCreator, \
    FixedCommission, PercentCommission, AccountCodes, DebitCreator, DepositCreator, CreditCreator, \
    Account, TransactionCodes
from src.checker import Checker
from src.clients import BaseClientBuilder, FullClientBuilder, ClientWithAddressBuilder, \
    ClientWithPassportBuilder, Client
from src.data_adapter import DataAdapter, UserNotExists, \
    UserAlreadyExists
from .io_implementation import IOImplementation


@dataclass
class IOAssistant:
    io_implementation: IOImplementation

    def print(self, *args):
        """Print lines in the output"""
        self.io_implementation.write(*args)

    def input(self) -> str:
        """Read one line from the input"""
        return self.io_implementation.read()

    def ask_code(self, max_code: int) -> int:
        success = False
        answer = None
        while not success:
            try:
                answer = int(self.input())
                if answer not in range(1, max_code + 1):
                    raise ValueError
            except ValueError:
                self.print(
                    f"Your answer should be {', '.join(str(i) for i in range(1, max_code))}" +
                    f" or {max_code}")
            else:
                success = True
            finally:
                if success:
                    return answer


@dataclass(init=False)
class AuthAssistant(IOAssistant):
    """Class helping with authentication"""
    _checker: Checker
    _user_data: list | None = None
    _with_passport: bool | None = None

    def __init__(self, io: IOImplementation, adapter: DataAdapter):
        super().__init__(io)
        self._checker = Checker(adapter)
        self._user_data = None
        self._with_passport = None

    def print_welcome(self):
        self.print("""\t\t\t\tWelcome to the bank system!\t\t\t\t""")

    def print_try_again(self):
        self.print("Error, please check your answer and try again.")

    def print_choice(self):
        self.print(
            """ Please, sign up or sign in(now and later choose the number to answer):
1)sign up
2)sign in""")

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
            self._checker.check_if_user_exists(new_client.name, new_client.surname)
        except UserNotExists:
            return new_client
        raise UserAlreadyExists

    def login(self) -> tuple[str, str] | None:
        success = False
        self.print("Enter your name and surname:")  # Todo: пароль?
        answer = self.input().split()
        try:
            assert len(answer) == 2
            self._checker.check_if_user_exists(*answer)
        except AssertionError:
            self.print("You name and surname should be only two words")
            log(WARNING, f"Attempt to sign in with incorrect name and surname: {' '.join(answer)}")
        except UserNotExists:
            self.print("There are not users with such name and surname")
            log(WARNING, f"There are not users with such name and surname: {' '.join(answer)}")
        else:
            success = True
        finally:
            if success:
                self.print("Sign in success")
                return answer[0], answer[1]

    def sign_up(self) -> Client:
        success = False
        new_client = None
        while not success:
            try:
                self.learn_about_user()
                new_client = self.generate_client()
            except AssertionError:
                self.print_try_again()
                log(WARNING, "Wrong user work_with_data in sign up")
            except ValueError:
                self.print_try_again()
                log(WARNING, "Not two words in name and surname")
            except UserAlreadyExists:
                self.print_try_again()
                log(WARNING, "Sign up to user already exist")
            else:
                success = True
        assert new_client is not None
        self.print("Sign up succeeded")
        return new_client


@dataclass(init=False)
class AssistantWithClient(IOAssistant):
    client: Client

    def __init__(self, io: IOImplementation):
        super().__init__(io)
        self.client = None

    @property
    def client(self) -> Client:
        if self._client is None:
            raise ClientIsNotSet
        return self._client

    @client.setter
    def client(self, val):
        self._client = val


class AccountsAssistant(AssistantWithClient):
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
        success = False
        end = None
        while not success:
            self.print("Enter the end of the period of account in format DD.MM.YYYY:")
            try:
                end = datetime.datetime.strptime(self.input(), "%d.%m.%Y")
            except ValueError:
                self.print("Your end of the account should be in format DD.MM.YYYY")
            else:
                success = True
        return end

    def get_commission(self):
        while True:
            self.print("Choose the type of the commission: fixed(1) or percent(2)")
            try:
                answer = int(self.input())
                if answer == 1:
                    self.print("Enter the value:")
                    return FixedCommission(int(self.input()))
                self.print("Enter the percent:")
                return PercentCommission(float(self.input()))
            except ValueError:
                self.print("Your answer should be an integer or a float(in percent commission)")

    def get_bank(self, banks: list[Bank]) -> Bank:
        self.print("Choose the bank to your account:")
        for i in range(1, len(banks) + 1):
            self.print(f"{i}) {banks[i - 1]}")
        code = self.ask_code(len(banks)) - 1
        return banks[code]

    def get_creator(self, account_type) -> AccountCreator:
        account_creator = None
        match account_type:
            case AccountCodes.DEBIT:
                account_creator = DebitCreator()
            case AccountCodes.DEPOSIT:
                account_creator = DepositCreator()
            case AccountCodes.CREDIT:
                account_creator = CreditCreator(self.get_commission())
        assert account_creator is not None
        return account_creator

    def choice_type_of_account(self) -> int:
        self.print("""Choose the type of the account:
1) Debit
2) Deposit
3) Credit""")
        return self.ask_code(3)

    def show_accounts(self):
        if self.client.have_accounts():
            self.print("Your accounts:")
            for ac in self.client.accounts:
                self.print(ac)
        else:
            self.print("You have not got accounts yet")

    def add_new_account(self, account: Account):
        self.client.add_account(account)


class ClientIsNotSet(Exception):
    pass


@dataclass
class MainAssistant(IOAssistant):
    def print_choice(self) -> int:
        q = "What do you want? View your accounts(1), created a new one(2)," \
            + " make a transaction(3) or exit(4)?"
        self.print(q)
        return self.ask_code(4)

    def print_bye(self):
        self.print("Good bye!")


class HaveNotAccountsYet(Exception):
    pass


@dataclass
class TransactionAssistant(AssistantWithClient):
    def __init__(self, io: IOImplementation):
        super().__init__(io)
        self._operator = Operator()

    def account_choice(self) -> Account:
        if not self.client.have_accounts():
            self.print("You have not accounts yet")
            raise HaveNotAccountsYet
        self.print("Choose your account:")
        for i in range(1, len(self.client.accounts) + 1):
            self.print(f"{i}) {self.client.accounts[i - 1]}")
        account = self.client.accounts[self.ask_code(len(self.client.accounts)) - 1]
        return account

    def print_choice(self) -> tuple[int, Account, float]:
        account = self.account_choice()
        self.print("What type of transaction you want: withdraw(1), put(2), transfer(3)?")
        code = self.ask_code(3)
        self.print("Enter the summa:")
        success = False
        summa = None
        while not success:
            try:
                summa = float(self.input())
                if not (summa * 100).is_integer():
                    raise ValueError
            except ValueError:
                self.print("Wrong format of the summa")
            else:
                success = True
        return code, account, summa

    def print_success(self):
        self.print("Transaction succeeded")

    def choice_operation(self, transaction_type: int, account: Account, summa: float):
        match transaction_type:
            case TransactionCodes.WITHDRAW:
                self._operator.make_withdraw(account, summa)
            case TransactionCodes.PUT:
                self._operator.make_put(account, summa)
            case TransactionCodes.TRANSFER:
                second_account = self.account_choice()
                self._operator.make_transfer(account, second_account, summa)
