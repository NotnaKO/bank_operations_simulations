import pytest

from src import DataAdapter, UserNotExists
from src.accounts import DeclinedOperation, Money
from src.checker import Checker, InvalidTransfer


def test_user_existing(tmpdir, create_base):
    with DataAdapter(tmpdir / "data.json") as adapt:
        check = Checker(adapt)
        check.check_if_client_exists_by_name("a", "a")
        check.check_if_client_exists_by_client(adapt.get_client("a a"))
        with pytest.raises(UserNotExists):
            check.check_if_client_exists_by_name("", "")


def test_transfer(tmpdir, create_base):
    with DataAdapter(tmpdir / "data.json") as adapt:
        check = Checker(adapt)
        with pytest.raises(DeclinedOperation, match="incomplete information"):
            check.approve_transfer(adapt.get_client("a b"), adapt.get_client("a b").accounts[1],
                                   adapt.get_client("a b").accounts[0], Money(2500))
        with pytest.raises(InvalidTransfer, match="same account"):
            check.approve_transfer(adapt.get_client("a a"), adapt.get_client("a a").accounts[0],
                                   adapt.get_client("a a").accounts[0], Money(250))
