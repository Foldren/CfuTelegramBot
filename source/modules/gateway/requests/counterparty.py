from dataclasses import dataclass


@dataclass
class CreateCounterpartyRequest:
    __slots__ = {"name", "inn", "categoryID"}
    name: str
    inn: str
    categoryID: int


@dataclass
class UpdateCounterpartyRequest:
    categoryID: int = None
    name: str = None
    inn: str = None


@dataclass
class DeleteCounterpartiesRequest:
    __slots__ = {"counterpartiesID"}
    counterpartiesID: list[int]
