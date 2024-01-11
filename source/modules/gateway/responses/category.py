from dataclasses import dataclass
from modules.gateway.responses.children import DCategory


@dataclass
class GetCategoriesResponse:
    __slots__ = {"categories"}
    categories: list[DCategory]
