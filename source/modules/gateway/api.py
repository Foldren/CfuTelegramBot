from dataclasses import asdict, dataclass
from httpx import AsyncClient
from modules.gateway.responses.auth import SignInResponse
from source.config import GATEWAY_PATH
from source.modules.gateway.requests.auth import SignInRequest
from source.modules.gateway.responses.rpc import RpcResponse, RpcExceptionResponse


class ApiGateway:
    main_path: str = GATEWAY_PATH
    headers = {'Content-Type': 'application/json'}

    def __init__(self, access_token: str = ""):
        """
        При инициализации нужно указать рабочий access_token для дальнейшей работы

        @param access_token: активный jwt токен
        """
        if access_token:
            self.headers['Authorization'] = 'Bearer ' + access_token

    async def request(self, method: str, url: str, request: dataclass, d_response_obj: dataclass) -> RpcResponse:
        async with AsyncClient(verify=False) as async_session:
            response = await async_session.request(
                method=method,
                url=self.main_path + url,
                headers=self.headers,
                json=asdict(request)
            )

            try:
                rpc_response = RpcResponse.from_dict(response.json())

                if rpc_response.data is not None:
                    rpc_response.data = d_response_obj.from_dict(rpc_response.data)
            except AttributeError:
                rpc_response = RpcExceptionResponse.from_dict(response.json())

        return rpc_response

    async def auth(self, email: str, password: str) -> RpcResponse:
        rpc_response = await self.request(
            method="post",
            url="/auth/sign-in",
            request=SignInRequest(email, password),
            d_response_obj=SignInResponse
        )

        return rpc_response


# if __name__ == "__main__":
#     ApiGateway(email="bbb@gmail.com", password="P@ssw0rd123!")
