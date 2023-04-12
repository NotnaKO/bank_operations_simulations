import json
import os
import pathlib
import shutil

import pytest

from src import DataAdapter


@pytest.fixture
def create_tmp_dir():
    os.mkdir("tmp")

    yield pathlib.Path("tmp")

    shutil.rmtree("tmp")


@pytest.fixture
def create_base(create_tmp_dir):
    data = {
        "abc": 1,
        "bcd": 2,
        "array": [1, 2, 3]
    }
    with open(create_tmp_dir / "data.json", "w") as file:
        json.dump(data, file)
    yield data


def test_data_safe(create_tmp_dir, create_base):
    file_name = create_tmp_dir / "data.json"
    try:
        with DataAdapter(file_name):
            raise RuntimeError
    except RuntimeError:
        with open(file_name) as file:
            assert json.load(file) == create_base
