import json
import pathlib
from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable

import pytest

from src import DataAdapter
from src.session import IOImplementation

data_path = pathlib.Path(__file__).parent / "data.json"


@pytest.fixture
def create_base(tmpdir):
    with open(data_path) as file:
        data = json.load(file)
    with open(tmpdir / "data.json", "w") as file:
        json.dump(data, file)
    yield data


@dataclass(init=False)
class IOtest(IOImplementation):
    answers: Deque[str]
    last_question: str = ""

    def __init__(self, deq: Deque[str] | None = None):
        super().__init__(None, None)
        if deq is None:
            self.answers = deque()
        else:
            self.answers = deq

    def read(self, *args, **kwargs) -> str:
        return self.answers.popleft()

    def write(self, *args, **kwargs) -> None:
        self.last_question = ' '.join(args)

    def push_answer(self, answer: str):
        self.answers.append(answer)

    def extend_answers(self, answers: Iterable[str]):
        self.answers.extend(answers)


class KillInput(Exception):
    pass


class IOWithKill(IOtest):
    timer: int = 0
    end: float | int = float("inf")

    def set_end(self, end: int):
        self.end = end

    def read(self, *args, **kwargs) -> str:
        self.timer += 1
        if self.timer >= self.end:
            raise KillInput(self.last_question)
        return super().read(*args, **kwargs)


@pytest.fixture
def adapter(tmpdir, create_base):
    with DataAdapter(tmpdir / "data.json") as adapt:
        return adapt


@pytest.fixture
def io_for_test():
    io = IOWithKill()
    yield io
