from abc import ABC, abstractmethod
from dataclasses import dataclass

from source.python.accounts.accounts import Debit, Account, Deposit, Credit
from source.python.session.assistants import AccountsAssistant


@dataclass
class AccountCreator(ABC):
    _assistant: AccountsAssistant

    @abstractmethod
    def create_account(self) -> Account:
        return Account(self._assistant.get_money(), self._assistant.get_end_of_period())


class DebitCreator(AccountCreator):
    def create_account(self) -> Debit:
        base_account = super().create_account()
        return Debit(base_account.balance, base_account.end)


class DepositCreator(AccountCreator):
    def create_account(self) -> Deposit:
        base_account = super().create_account()
        return Deposit(base_account.balance, base_account.end)


class CreditCreator(AccountCreator):
    def create_account(self) -> Credit:
        base_account = super().create_account()
        return Credit(base_account.balance, base_account.end, self._assistant.get_commission())
