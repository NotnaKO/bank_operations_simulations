import pytest

from src import UserNotExists
from src.accounts import DeclinedOperation, Money
from src.checker import Checker, InvalidTransfer


def test_user_existing(adapter):
    check = Checker(adapter)
    check.check_if_client_exists_by_name("a", "a")
    check.check_if_client_exists_by_client(adapter.get_client("a a"))
    with pytest.raises(UserNotExists):
        check.check_if_client_exists_by_name("", "")


def test_transfer(adapter):
    check = Checker(adapter)
    with pytest.raises(DeclinedOperation, match="incomplete information"):
        check.approve_transfer(adapter.get_client("a b"), adapter.get_client("a b").accounts[1],
                               adapter.get_client("a b").accounts[0], Money(2500))
    with pytest.raises(InvalidTransfer, match="same account"):
        check.approve_transfer(adapter.get_client("a a"), adapter.get_client("a a").accounts[0],
                               adapter.get_client("a a").accounts[0], Money(250))
