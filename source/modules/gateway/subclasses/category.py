from components.tools import Tool
from modules.gateway.api import ApiGateway
from modules.gateway.requests.category import GetCategoriesRequest, CreateCategoryRequest, UpdateCategoryRequest, \
    DeleteCategoriesRequest
from modules.gateway.responses.category import GetCategoriesResponse, CreateCategoryResponse, UpdateCategoryResponse, \
    DeleteCategoriesResponse
from modules.gateway.responses.children import DCategory


class ApiCategory(ApiGateway):
    async def get(self, parent_id: int = None) -> list[DCategory]:
        rpc_response: GetCategoriesResponse = await super()._request(
            method="get",
            url="/categories",
            request_obj=GetCategoriesRequest(parentID=parent_id),
            response_obj=GetCategoriesResponse
        )

        return rpc_response.categories

    async def create(self, name: str, parent_id: int = None) -> CreateCategoryResponse:
        rpc_response = await super()._request(
            method="post",
            url="/categories",
            request_obj=CreateCategoryRequest(name=name, parentID=parent_id),
            response_obj=CreateCategoryResponse
        )

        return rpc_response

    async def update(self, category_id: int, name: str = None,
                     status: int = None) -> UpdateCategoryResponse:
        rpc_response = await super()._request(
            method="patch",
            url=f"/categories/{category_id}",
            request_obj=UpdateCategoryRequest(name=name, status=status),
            response_obj=UpdateCategoryResponse
        )

        return rpc_response

    async def delete(self, categories_id: list[int]) -> DeleteCategoriesResponse:
        params_url = await Tool.generate_param_url(start_url="/categories", params_name="categoriesID",
                                                   params=categories_id)

        rpc_response = await super()._request(
            method="delete",
            url=params_url,
            request_obj=DeleteCategoriesRequest(categoriesID=categories_id),
            response_obj=DeleteCategoriesResponse,
            data_in_url=True
        )

        return rpc_response
