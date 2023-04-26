import json

import pytest

from src import BankNotExists, DataAdapter, UserNotExists


def test_data_safety(tmpdir, create_base):
    file_name = tmpdir / "data.json"
    try:
        with DataAdapter(file_name):
            raise RuntimeError
    except RuntimeError:
        with open(file_name) as file:
            assert json.load(file) == create_base
    else:
        assert False


def test_encoder_for_search(tmpdir, create_base):
    file_name = tmpdir / "data.json"
    with DataAdapter(file_name) as adapt:
        assert adapt.get_client("a a")._address == "ad"
        assert adapt.get_bank("Sberbank").name == "Sberbank"


def test_encoder_for_exceptions(tmpdir, create_base):
    file_name = tmpdir / "data.json"
    with DataAdapter(file_name) as adapt:
        with pytest.raises(UserNotExists):
            adapt.get_client("not exist")
        with pytest.raises(BankNotExists):
            adapt.get_bank("not exists")
