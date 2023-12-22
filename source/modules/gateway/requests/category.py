from dataclasses import dataclass


@dataclass
class GetCategoriesRequest:
    email: str
    password: str
