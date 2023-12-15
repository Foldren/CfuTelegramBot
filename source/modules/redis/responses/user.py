from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class GetUserResponse(DataClassJsonMixin):
    __slots__ = {"chatID"}
    chatID: str
