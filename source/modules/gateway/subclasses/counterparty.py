from components.tools import Tool
from modules.gateway.api import ApiGateway
from modules.gateway.requests.counterparty import CreateCounterpartyRequest, DeleteCounterpartiesRequest
from modules.gateway.responses.counterparty import GetCounterpartiesResponse, CreateCounterpartyResponse, \
    DeleteCounterpartiesResponse


class ApiCounterparty(ApiGateway):
    async def get(self) -> GetCounterpartiesResponse:
        rpc_response = await self._request(
            method="get",
            url="/counterparties",
            response_obj=GetCounterpartiesResponse
        )

        return rpc_response

    async def create(self, inn: int, name: str, category_id: int) -> CreateCounterpartyResponse:
        rpc_response = await super()._request(
            method="post",
            url="/counterparties",
            request_obj=CreateCounterpartyRequest(inn=inn, name=name, categoryID=category_id),
            response_obj=CreateCounterpartyResponse
        )

        return rpc_response

    # async def update(self, category_id: int, name: str = None,
    #                  status: int = None) -> UpdateCategoryResponse:
    #     rpc_response = await super()._request(
    #         method="patch",
    #         url=f"/categories/{category_id}",
    #         request_obj=UpdateCategoryRequest(name=name, status=status),
    #         response_obj=UpdateCategoryResponse
    #     )
    #
    #     return rpc_response
    #

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
