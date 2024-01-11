from dataclasses import asdict, dataclass
from traceback import print_exc

import jwt
from httpx import AsyncClient, ReadTimeout, Cookies
from modules.gateway.requests.category import GetCategoriesRequest
from modules.gateway.responses.auth import SignInResponse, RefreshResponse
from modules.gateway.responses.category import GetCategoriesResponse
from source.config import GATEWAY_PATH, JWT_SECRET
from source.modules.gateway.requests.auth import SignInRequest
from source.modules.gateway.responses.rpc import RpcResponse, RpcExceptionResponse


class ApiGateway:
    main_path: str = GATEWAY_PATH
    headers = {'Content-Type': 'application/json'}
    cookies: Cookies
    user_chat_id: int

    def __init__(self, user_chat_id: int = None,  access_token: str = "", cookies: Cookies = None):
        """
        При инициализации нужно указать рабочий access_token для дальнейшей работы
        @param access_token: активный jwt токен
        """
        if access_token:
            self.headers['Authorization'] = 'Bearer ' + access_token
        if cookies:
            self.cookies = cookies
        if user_chat_id:
            self.user_chat_id = user_chat_id

    async def __refresh(self):
        async with AsyncClient(verify=False) as async_session:
            response_token = await async_session.post(
                url=self.main_path + "/auth/refresh",
                headers=self.headers,
            )
            print(response_token.json())
            print(jwt.decode(self.headers['Authorization'].split(" ")[1], JWT_SECRET, algorithms=["HS256"]))
            d_response: RefreshResponse = RefreshResponse.from_dict(response_token.json())
            print(2)

            self.headers['Authorization'] = 'Bearer ' + d_response.data.accessToken

    async def __request(self, method: str, url: str, request_obj: dataclass, response_obj: dataclass) -> RpcResponse:
        async with AsyncClient(verify=False) as async_session:
            # Пробуем выполнить запрос
            try:
                response = await async_session.request(
                    method=method,
                    url=self.main_path + url,
                    headers=self.headers,
                    json=asdict(request_obj),
                    timeout=1
                )
                print(1)
                print(response.json())

            except ReadTimeout:
                # В случае таймаута обновляем токен
                # await self.__refresh()
                print_exc()


                # Снова выполняем запрос
                # response = await async_session.request(
                #     method=method,
                #     url=self.main_path + url,
                #     headers=self.headers,
                #     json=asdict(request_obj),
                # )

            try:
                rpc_response = RpcResponse.from_dict(response.json())

                if rpc_response.data is not None:
                    rpc_response.data = response_obj.from_dict(rpc_response.data)
            except AttributeError:
                rpc_response = RpcExceptionResponse.from_dict(response.json())

        return rpc_response

    async def auth(self, email: str, password: str) -> RpcResponse:
        rpc_response = await self.__request(
            method="post",
            url="/auth/sign-in",
            request_obj=SignInRequest(email, password),
            response_obj=SignInResponse
        )

        return rpc_response

    async def get_categories(self, user_id: int, parent_id: int = None) -> RpcResponse:
        rpc_response = await self.__request(
            method="get",
            url="/categories",
            request_obj=GetCategoriesRequest(user_id, parent_id),
            response_obj=GetCategoriesResponse
        )

        return rpc_response

# if __name__ == "__main__":
#     run(ApiGateway().auth(email="bbb@gmail.com", password="P@ssw0rd123!"))
