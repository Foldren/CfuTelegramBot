from dataclasses import dataclass


@dataclass
class GetCategoriesRequest:
    __slots__ = {"userID", "parentID"}
    userID: int
    parentID: int
