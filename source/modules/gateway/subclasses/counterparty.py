from components.tools import Tool
from modules.gateway.api import ApiGateway
from modules.gateway.requests.counterparty import CreateCounterpartyRequest, DeleteCounterpartiesRequest, \
    UpdateCounterpartyRequest
from modules.gateway.responses.children import DCounterparty
from modules.gateway.responses.counterparty import GetCounterpartiesResponse, CreateCounterpartyResponse, \
    DeleteCounterpartiesResponse, UpdateCounterpartyResponse


class ApiCounterparty(ApiGateway):
    async def get(self) -> list[DCounterparty]:
        rpc_response: GetCounterpartiesResponse = await self._request(
            method="get",
            url="/counterparties",
            response_obj=GetCounterpartiesResponse
        )

        return rpc_response.counterparties

    async def create(self, inn: str, name: str, category_id: int) -> CreateCounterpartyResponse:
        rpc_response = await super()._request(
            method="post",
            url="/counterparties",
            request_obj=CreateCounterpartyRequest(inn=inn, name=name, categoryID=category_id),
            response_obj=CreateCounterpartyResponse
        )

        return rpc_response

    async def update(self, counterparty_id: int, category_id: int = None,
                     name: str = None, inn: str = None) -> UpdateCounterpartyResponse:
        rpc_response = await super()._request(
            method="patch",
            url=f"/counterparties/{counterparty_id}",
            request_obj=UpdateCounterpartyRequest(categoryID=category_id, name=name, inn=inn),
            response_obj=UpdateCounterpartyResponse
        )

        return rpc_response

    async def delete(self, counterparties_id: list[int]) -> DeleteCounterpartiesResponse:
        params_url = await Tool.generate_param_url(start_url="/counterparties", params_name="counterpartiesID",
                                                   params=counterparties_id)

        rpc_response = await super()._request(
            method="delete",
            url=params_url,
            request_obj=DeleteCounterpartiesRequest(counterpartiesID=counterparties_id),
            response_obj=DeleteCounterpartiesResponse,
            data_in_url=True
        )

        return rpc_response
