from dataclasses import dataclass
from typing import Any
from dataclasses_json import DataClassJsonMixin


@dataclass
class RpcError(DataClassJsonMixin):
    __slots__ = {"message", "statusCode"}
    message: str
    statusCode: int


@dataclass()
class RpcResponse(DataClassJsonMixin):
    data: Any = None
    error: RpcError = None
