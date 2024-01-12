from dataclasses import asdict, dataclass
from typing import Union, Any
from aiogram.types import Message, CallbackQuery
from httpx import AsyncClient, ReadTimeout, Cookies
from components.tools import Tool
from modules.gateway.requests.category import GetCategoriesRequest
from modules.gateway.responses.auth import SignInResponse, RefreshResponse
from modules.gateway.responses.category import GetCategoriesResponse
from modules.redis.redis import Redis
from source.config import GATEWAY_PATH
from source.modules.gateway.requests.auth import SignInRequest


class ApiGateway:
    main_path: str = GATEWAY_PATH
    headers = {'Content-Type': 'application/json'}
    redis: Redis
    event: Union[Message, CallbackQuery]

    def __init__(self, redis: Redis, event: Union[Message, CallbackQuery]):
        """
        При инициализации подключаем redis и передаем event
        :param redis: бд redis
        :param event: объект колбека или сообщения
        """
        self.redis = redis
        self.event = event

    async def __refresh(self):
        chat_id = await Tool.get_chat_id(self.event)
        user = await self.redis.user.get(chat_id)

        async with AsyncClient(verify=False, cookies=user.cookies) as async_session:
            response_token = await async_session.post(
                url=self.main_path + "/auth/refresh",
                headers=self.headers,
            )

            d_response: RefreshResponse = RefreshResponse.from_dict(response_token.json())

            # Обновляем access_token
            access_token = d_response.data.accessToken
            self.headers['Authorization'] = 'Bearer ' + access_token

            await self.redis.user.set(
                chat_id=self.event.from_user.id,
                access_token=access_token,
                cookies=response_token.cookies
            )

    async def __request(self, method: str, url: str, request_obj: dataclass, response_obj: dataclass) -> Any:
        # Прикрепляем текущий токен
        chat_id = await Tool.get_chat_id(event=self.event)
        user = await self.redis.user.get(chat_id)
        self.headers['Authorization'] = 'Bearer ' + user.accessToken

        async with AsyncClient(verify=False, cookies=user.cookies, headers=self.headers) as async_session:
            # Пробуем выполнить запрос
            try:
                response = await async_session.request(
                    method=method,
                    url=self.main_path + url,
                    json=asdict(request_obj),
                    timeout=1,
                )

            except ReadTimeout:
                # Обновляем токен в случае задержки
                await self.__refresh()

                # Снова выполняем запрос
                response = await async_session.request(
                    method=method,
                    url=self.main_path + url,
                    json=asdict(request_obj),
                )

            # Проверяем на ошибки
            rpc_response = await Tool.handle_exceptions(response, self.event, response_obj)

        return rpc_response

    async def auth(self, email: str, password: str) -> SignInResponse:
        async with AsyncClient(verify=False) as async_session:
            response = await async_session.post(
                url=self.main_path + "/auth/sign-in",
                headers=self.headers,
                json=asdict(SignInRequest(email, password)),
            )

        rpc_response = await Tool.handle_exceptions(response, self.event, SignInResponse)

        # Сохраняем токен
        self.headers['Authorization'] = 'Bearer ' + rpc_response.accessToken

        # Записываем данные
        await self.redis.user.set(
            chat_id=self.event.chat.id,
            access_token=rpc_response.accessToken,
            cookies=response.cookies
        )

        return rpc_response

    async def get_categories(self, user_id: int, parent_id: int = None) -> GetCategoriesResponse:
        rpc_response = await self.__request(
            method="get",
            url="/categories",
            request_obj=GetCategoriesRequest(user_id, parent_id),
            response_obj=GetCategoriesResponse
        )

        return rpc_response

# if __name__ == "__main__":
#     run(ApiGateway().auth(email="bbb@gmail.com", password="P@ssw0rd123!"))
