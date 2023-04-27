import json
import pathlib
from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable, List

import pytest

from src import DataAdapter
from src.session import IOImplementation, SessionFacade

data_path = pathlib.Path(__file__).parent / "data.json"

sequence_to_create_tmp_client = ["1", "tmp tmp", '', '']
sequence_to_create_complete_client = ["1", "tmp tmp", 'address', 'passport']
sequence_to_log_in_with_tmp = ["2", "tmp tmp"]
sequence_to_create_debit = ["1", "5000", "05.08.2024", "1"]
sequence_to_create_credit = ['3', '1', '5', '5000', '01.01.2004', '3']


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
    questions: List[str]

    def __init__(self, deq: Deque[str] | None = None):
        super().__init__(None, None)
        if deq is None:
            self.answers = deque()
        else:
            self.answers = deq
        self.questions = []

    def read(self, *args, **kwargs) -> str:
        return self.answers.popleft()

    @property
    def last_question(self):
        return self.questions[-1]

    def write(self, *args, **kwargs) -> None:
        self.questions.append(str(' '.join(args)))

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

    def reset(self):
        self.timer = 0

    def read(self, *args, **kwargs) -> str:
        self.timer += 1
        if self.timer >= self.end or len(self.answers) == 0:
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


@pytest.fixture
def session(adapter, io_for_test):
    return SessionFacade(adapter, io_for_test)
