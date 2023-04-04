import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass


class InputImplementation(ABC):
    @abstractmethod
    def read(self, *args, **kwargs) -> str:
        pass


class OutputImplementation(ABC):
    @abstractmethod
    def write(self, *args, **kwargs) -> None:
        pass


@dataclass
class IOImplementation:
    _in: InputImplementation
    _out: OutputImplementation

    def write(self, *args, **kwargs) -> None:
        self._out.write(*args, **kwargs)

    def read(self, *args, **kwargs) -> str:
        return self._in.read(*args, **kwargs)


class ConsoleInput(InputImplementation):
    def read(self, *args, **kwargs) -> str:
        return sys.stdin.readline().rstrip()


class ConsoleOutput(OutputImplementation):
    def write(self, *args, **kwargs) -> None:
        print(*args)


@dataclass(init=False)
class StandardConsoleIO(IOImplementation):
    _in: ConsoleInput
    _out: ConsoleOutput

    def __init__(self):
        super().__init__(ConsoleInput(), ConsoleOutput())
