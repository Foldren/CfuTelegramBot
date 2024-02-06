from dataclasses import dataclass


@dataclass
class GetCategoriesRequest:
    userID: str
    parentID: int = None


@dataclass
class CreateCategoryRequest:
    userID: str
    name: str
    parentID: int = None
