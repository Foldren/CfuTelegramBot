from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class UserData(DataClassJsonMixin):
    __slots__ = {"accessToken", "fio"}
    accessToken: str
    fio: str
