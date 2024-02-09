from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class AuthorizationMessage(DataClassJsonMixin):
    __slots__ = {"email", "password"}
    email: str
    password: str


@dataclass
class CreateCounterpartyMessage(DataClassJsonMixin):
    __slots__ = {"inn", "name"}
    inn: int
    name: str
