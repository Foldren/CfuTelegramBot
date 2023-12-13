from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from modules.gateway.responses.children import DUser


@dataclass
class SignInResponse(DataClassJsonMixin):
    __slots__ = {"message", "statusCode"}
    accessToken: str
    user: DUser
