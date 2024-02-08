from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class GetCategoriesCallback(DataClassJsonMixin):
    __slots__ = {"id", "name"}
    id: int
    name: str


@dataclass
class GetCategoriesUpdateCallback(DataClassJsonMixin):
    __slots__ = {"id", "name", "status"}
    id: int
    name: str
    status: bool
