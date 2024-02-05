from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class AuthorizationMessage(DataClassJsonMixin):
    email: str = None
    password: str = None
