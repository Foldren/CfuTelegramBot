from modules.gateway.api import ApiGateway
from modules.gateway.requests.counterparty import CreateCounterpartyRequest
from modules.gateway.responses.counterparty import GetCounterpartiesResponse, CreateCounterpartyResponse


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
    #
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
    # async def delete(self, categories_id: list[int]) -> DeleteCategoriesResponse:
    #     params_url = await Tool.generate_param_url(start_url="/categories", params_name="categoriesID",
    #                                                params=categories_id)
    #
    #     rpc_response = await super()._request(
    #         method="delete",
    #         url=params_url,
    #         request_obj=DeleteCategoriesRequest(categoriesID=categories_id),
    #         response_obj=DeleteCategoriesResponse,
    #         data_in_url=True
    #     )
    #
    #     return rpc_response