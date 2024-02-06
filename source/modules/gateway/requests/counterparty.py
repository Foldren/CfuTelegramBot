from dataclasses import dataclass


@dataclass
class GetCounterpartiesRequest:
    __slots__ = {"userID"}
    userID: str
