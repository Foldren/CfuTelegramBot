from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class DUser(DataClassJsonMixin):
    __slots__ = {"email", "fio", "phoneNumber", "displayName", "role", "subscription", "tariff"}
    email: str
    fio: str
    phoneNumber: str
    displayName: str
    role: str
    subscription: list
    tariff: str


@dataclass
class DCategory(DataClassJsonMixin):
    __slots__ = {"id", "name", "status", "hasChildren"}
    id: int
    name: str
    status: int
    hasChildren: int


@dataclass
class DCounterparty(DataClassJsonMixin):
    id: int
    name: str
    inn: str
    categoryID: int = None
    categoryName: str = None
