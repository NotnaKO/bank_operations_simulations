from dataclasses import dataclass


@dataclass
class ReliabilityType:
    pass


class Reliable(ReliabilityType):
    pass


class NotReliable(ReliabilityType):
    pass
