import json
import pathlib

import pytest

data_path = pathlib.Path(__file__).parent / "data.json"


@pytest.fixture
def create_base(tmpdir):
    with open(data_path) as file:
        data = json.load(file)
    with open(tmpdir / "data.json", "w") as file:
        json.dump(data, file)
    yield data
