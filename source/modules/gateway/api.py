from dataclasses import asdict, dataclass
from typing import Union, Any
import jwt
from aiogram.types import Message, CallbackQuery
from dataclasses_json import DataClassJsonMixin
from httpx import AsyncClient
from jwt import ExpiredSignatureError
from components.tools import Tool
from modules.gateway.requests.category import GetCategoriesRequest
from modules.gateway.responses.auth import SignInResponse, RefreshResponse
from modules.gateway.responses.category import GetCategoriesResponse
from modules.redis.models import User
from source.config import GATEWAY_PATH, JWT_SECRET
from source.modules.gateway.requests.auth import SignInRequest


class ApiGateway:
    main_path: str = GATEWAY_PATH
    headers = {}
    event: Union[Message, CallbackQuery]

    def __init__(self, event: Union[Message, CallbackQuery]):
        """
        При инициализации передаем event
        :param event: объект колбека или сообщения
        """
        self.event = event

    async def __refresh(self):
        chat_id = await Tool.get_chat_id(self.event)
        user = await User.find(User.chat_id == chat_id).first()

        async with AsyncClient(verify=False, cookies=user.cookies) as async_session:
            response_token = await async_session.post(
                url=self.main_path + "/auth/refresh",
                headers=self.headers,
            )

            await Tool.handle_exceptions(response_token, self.event, RefreshResponse)

            d_response: RefreshResponse = RefreshResponse.from_dict(response_token.json())

            # Обновляем access_token
            access_token = d_response.data.accessToken
            self.headers['Authorization'] = 'Bearer ' + access_token

            await User(
                chat_id=self.event.from_user.id,
                accessToken=access_token,
                cookies=response_token.cookies
            ).save()

    async def __request(self, method: str, url: str, request_obj: dataclass, response_obj) -> Any:
        # Прикрепляем текущий токен
        chat_id = await Tool.get_chat_id(event=self.event)
        user = await User.find(User.chat_id == chat_id).first()
        self.headers['Authorization'] = 'Bearer ' + user.accessToken

        async with AsyncClient(verify=False, cookies=user.cookies, headers=self.headers) as async_session:
            # Пробуем выполнить запрос
            try:
                print(asdict(request_obj, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
                jwt.decode(user.accessToken, JWT_SECRET, algorithms=["HS256"])
                response = await async_session.request(
                    method=method,
                    url=self.main_path + url,
                    json=asdict(request_obj, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
                    if method == "post" else None,
                    params=asdict(request_obj, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
                    if method != "post" else None,
                )

            except ExpiredSignatureError:
                # Обновляем токен в случае задержки
                await self.__refresh()

                # Снова выполняем запрос
                response = await async_session.request(
                    method=method,
                    url=self.main_path + url,
                    json=asdict(request_obj) if method == "post" else None,
                    params=asdict(request_obj) if method != "post" else None,
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
        response.cookies.set('Secure', "")
        response.cookies.set('HttpOnly', "")

        # Записываем данные
        await User(
            chat_id=self.event.chat.id,
            accessToken=rpc_response.accessToken,
            cookies=response.cookies
        ).save()

        return rpc_response

    async def get_categories(self, chat_id: int, parent_id: int = None) -> GetCategoriesResponse:
        user = await User.find(User.chat_id == chat_id).first()
        user_data = jwt.decode(user.accessToken, JWT_SECRET, algorithms=["HS256"], options={"verify_signature": False})

        rpc_response = await self.__request(
            method="get",
            url="/categories",
            request_obj=GetCategoriesRequest(userID=user_data["id"], parentID=parent_id),
            response_obj=GetCategoriesResponse
        )

        return rpc_response
