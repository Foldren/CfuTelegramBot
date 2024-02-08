from modules.gateway.api import ApiGateway
from modules.gateway.requests.category import GetCategoriesRequest, CreateCategoryRequest, UpdateCategoryRequest
from modules.gateway.responses.category import GetCategoriesResponse, CreateCategoryResponse, UpdateCategoryResponse


class ApiCategory(ApiGateway):
    async def get(self, parent_id: int = None) -> GetCategoriesResponse:
        rpc_response = await super()._request(
            method="get",
            url="/categories",
            request_obj=GetCategoriesRequest(parentID=parent_id),
            response_obj=GetCategoriesResponse
        )

        return rpc_response

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
