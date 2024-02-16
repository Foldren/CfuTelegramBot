from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


# message --------------------------------------------------------------------------------------------------------------


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


# dialog_data ----------------------------------------------------------------------------------------------------------

@dataclass
class DialogCategory(DataClassJsonMixin):
    __slots__ = {"id", "name", "status", "hasChildren"}
    id: int
    name: str
    status: int
    hasChildren: int


@dataclass
class DialogCounterparty(DataClassJsonMixin):
    __slots__ = {"id", "name", "inn", "categoryID", "categoryName"}
    id: int
    name: str
    inn: str
    categoryID: int
    categoryName: str
