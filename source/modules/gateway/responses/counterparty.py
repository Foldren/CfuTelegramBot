from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from modules.gateway.responses.children import DCounterparty


@dataclass
class GetCounterpartiesResponse(DataClassJsonMixin):
    __slots__ = {"counterparties"}
    counterparties: list[DCounterparty]


@dataclass
class CreateCounterpartyResponse(DataClassJsonMixin):
    __slots__ = {"id"}
    id: int


@dataclass
class UpdateCounterpartyResponse(DataClassJsonMixin):
    __slots__ = {"id"}
    id: int


@dataclass
class DeleteCounterpartiesResponse(DataClassJsonMixin):
    __slots__ = {"counterpartiesID"}
    counterpartiesID: list[int]
