from abc import ABC


class Codes(ABC):
    """Class to provide codes for user in project"""


class TransactionCodes(Codes):
    WITHDRAW = 1
    PUT = 2
    TRANSFER = 3


class AccountCodes(Codes):
    DEBIT = 1
    DEPOSIT = 2
    CREDIT = 3


class ActionsCodes(Codes):
    SIGN_IN = 7
    SIGN_UP = 6
    COMPLETE_INFORMATION = 5
    SHOW_ACCOUNTS = 1
    CREATE_NEW_ACCOUNT = 2
    MAKE_TRANSACTION = 3
    EXIT = 4
