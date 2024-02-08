from dataclasses import dataclass


@dataclass
class GetCategoriesRequest:
    parentID: int = None


@dataclass
class CreateCategoryRequest:
    name: str
    parentID: int = None


@dataclass
class UpdateCategoryRequest:
    name: str = None
    status: int = None
