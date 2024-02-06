from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from modules.gateway.responses.children import DCounterparty


@dataclass
class GetCounterpartiesResponse(DataClassJsonMixin):
    __slots__ = {"counterparties"}
    counterparties: list[DCounterparty]
