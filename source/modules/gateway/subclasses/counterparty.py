from modules.gateway.api import ApiGateway
from modules.gateway.requests.counterparty import GetCounterpartiesRequest
from modules.gateway.responses.counterparty import GetCounterpartiesResponse


class ApiCounterParty(ApiGateway):
    async def get(self, chat_id: int) -> GetCounterpartiesResponse:
        user_id = await self._get_user_id(chat_id)
        rpc_response = await self._request(
            method="get",
            url="/counterparties",
            request_obj=GetCounterpartiesRequest(userID=user_id),
            response_obj=GetCounterpartiesResponse
        )

        return rpc_response
