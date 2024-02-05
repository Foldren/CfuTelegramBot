from dataclasses import dataclass


@dataclass
class GetCategoriesRequest:
    userID: str
    parentID: int = None
