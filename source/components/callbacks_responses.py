from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class GetCategoriesCallback(DataClassJsonMixin):
    id: int
    name: str
    status: int = None
    hasChildren: bool = None


@dataclass
class GetCategoriesUpdateCallback(DataClassJsonMixin):
    __slots__ = {"id", "name", "status"}
    id: int
    name: str
    status: int
