from dataclasses import dataclass


@dataclass
class CreateCounterpartyRequest:
    __slots__ = {"name", "inn", "categoryID"}
    name: str
    inn: int
    categoryID: int


@dataclass
class UpdateCounterPartyRequest:
    counterpartyID: int
    categoryID: int = None
    name: str = None
    inn: int = None


@dataclass
class DeleteCounterpartiesRequest:
    __slots__ = {"counterpartiesID"}
    counterpartiesID: list[int]
