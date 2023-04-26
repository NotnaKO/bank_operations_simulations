import json

import pytest


@pytest.fixture
def create_base(tmpdir):
    with open("data.json") as file:
        data = json.load(file)
    with open(tmpdir / "data.json", "w") as file:
        json.dump(data, file)
    yield data
