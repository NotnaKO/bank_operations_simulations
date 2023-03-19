from abc import ABC, abstractmethod
from dataclasses import dataclass

from source.python.accounts.accounts import Debit, Account, Deposit, Credit
from source.python.accounts.banks import Bank
from source.python.session.assistants import AccountsAssistant


@dataclass
class AccountCreator(ABC):
    _assistant: AccountsAssistant

    @abstractmethod
    def create_account(self, banks: list[Bank]) -> Account:
        return Account(self._assistant.get_money(), self._assistant.get_end_of_period(),
                       self._assistant.get_bank(banks).name)


class DebitCreator(AccountCreator):
    def create_account(self, banks: list[Bank]) -> Debit:
        base_account = super().create_account(banks)
        return Debit(base_account.balance, base_account.end, base_account.bank_name)


class DepositCreator(AccountCreator):
    def create_account(self, banks: list[Bank]) -> Deposit:
        base_account = super().create_account(banks)
        return Deposit(base_account.balance, base_account.end, base_account.bank_name)


class CreditCreator(AccountCreator):
    def create_account(self, banks: list[Bank]) -> Credit:
        base_account = super().create_account(banks)
        return Credit(base_account.balance, base_account.end, self._assistant.get_commission(),
                      base_account.bank_name)
