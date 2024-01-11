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
class DCategory:
    __slots__ = {"id", "name", "status"}
    id: int
    name: str
    status: bool


@dataclass
class DToken:
    __slots__ = {"accessToken"}
    accessToken: str
