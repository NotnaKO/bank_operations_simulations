from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

from src.accounts.accounts import Account, Commission, Credit, Debit, Deposit


@dataclass
class AccountCreator(ABC):
    @abstractmethod
    def create_account(self, money: float, end: date,
                       bank_name: str) -> Account:
        pass


class DebitCreator(AccountCreator):
    def create_account(self, money: float, end: date,
                       bank_name: str) -> Debit:
        return Debit(money, end, bank_name)


class DepositCreator(AccountCreator):
    def create_account(self, money: float, end: date,
                       bank_name: str) -> Deposit:
        return Deposit(money, end, bank_name)


@dataclass
class CreditCreator(AccountCreator):
    commission: Commission

    def create_account(self, money: float, end: date,
                       bank_name: str) -> Credit:
        return Credit(money, end, self.commission,
                      bank_name)
