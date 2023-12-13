from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class DUser(DataClassJsonMixin):
    __slots__ = {"email", "fio", "phoneNumber", "displayName", "role", "subscription", "tariff", "email", "fio"}
    phoneNumber: str
    displayName: str
    role: str
    subscription: list
    tariff: str