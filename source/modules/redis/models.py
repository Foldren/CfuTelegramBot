from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class User(DataClassJsonMixin):
    pk: int  # chat_id
    role: str
    accessToken: str
    cookies: dict
