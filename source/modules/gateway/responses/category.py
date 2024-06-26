from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from modules.gateway.responses.children import DCategory


@dataclass
class GetCategoriesResponse(DataClassJsonMixin):
    __slots__ = {"categories"}
    categories: list[DCategory]


@dataclass
class CreateCategoryResponse(DataClassJsonMixin):
    __slots__ = {"id"}
    id: int


@dataclass
class UpdateCategoryResponse(DataClassJsonMixin):
    __slots__ = {"id"}
    id: int


@dataclass
class DeleteCategoriesResponse(DataClassJsonMixin):
    __slots__ = {"categoriesID"}
    categoriesID: list[int]
