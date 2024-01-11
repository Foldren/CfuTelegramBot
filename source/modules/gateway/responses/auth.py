from dataclasses import dataclass
from typing import Optional
from dataclasses_json import DataClassJsonMixin
from httpx import Cookies
from modules.gateway.responses.children import DUser, DToken


@dataclass
class SignInResponse(DataClassJsonMixin):
    accessToken: str
    user: DUser
    cookies: Optional[Cookies] = None


@dataclass
class RefreshResponse(DataClassJsonMixin):
    __slots__ = {"data"}
    data: DToken
