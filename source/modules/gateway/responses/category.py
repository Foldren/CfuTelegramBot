from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from modules.gateway.responses.children import DCategory


@dataclass
class GetCategoriesResponse(DataClassJsonMixin):
    __slots__ = {"categories"}
    categories: list[DCategory]
