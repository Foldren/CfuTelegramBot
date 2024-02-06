from dataclasses import asdict, dataclass
from typing import Union, Any
import jwt
from aiogram.types import Message, CallbackQuery
from httpx import AsyncClient
from jwt import ExpiredSignatureError
from components.tools import Tool
from modules.gateway.requests.category import GetCategoriesRequest, CreateCategoryRequest
from modules.gateway.requests.counterparty import GetCounterpartiesRequest
from modules.gateway.responses.auth import SignInResponse, RefreshResponse
from modules.gateway.responses.category import GetCategoriesResponse, CreateCategoryResponse
from modules.gateway.responses.counterparty import GetCounterpartiesResponse
from modules.redis.models import User
from source.config import GATEWAY_PATH, JWT_SECRET
from source.modules.gateway.requests.auth import SignInRequest


class ApiGateway:
    main_path: str = GATEWAY_PATH
    headers = {"User-Agent": "PostmanRuntime/7.36.1"}
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

        self.headers.pop('Authorization')

        async with AsyncClient(verify=True) as async_session:
            response_token = await async_session.post(
                url=self.main_path + "/auth/refresh",
                headers=self.headers,
                cookies=user.cookies
            )

            refresh_response = await Tool.handle_exceptions(response_token, self.event, RefreshResponse)

            # Обновляем access_token
            access_token = refresh_response.accessToken
            self.headers['Authorization'] = 'Bearer ' + access_token

            user.accessToken = access_token
            print(user.cookies)
            user.cookies = response_token.cookies.__dict__
            await user.save()

    async def __request(self, method: str, url: str, request_obj: dataclass, response_obj) -> Any:
        # Прикрепляем текущий токен
        chat_id = await Tool.get_chat_id(event=self.event)
        user = await User.find(User.chat_id == chat_id).first()
        self.headers['Authorization'] = 'Bearer ' + user.accessToken

        async with AsyncClient(verify=False, cookies=user.cookies, headers=self.headers) as async_session:
            # Пробуем выполнить запрос
            try:
                jwt.decode(user.accessToken, JWT_SECRET, algorithms=["HS256"])
                dict_params = asdict(request_obj, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
                response = await async_session.request(
                    method=method,
                    url=self.main_path + url,
                    json=dict_params if method == "post" else None,
                    params=dict_params if method != "post" else None,
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

    @staticmethod
    async def __get_user_id(chat_id: int):
        user = await User.find(User.chat_id == chat_id).first()
        user_data = jwt.decode(user.accessToken, JWT_SECRET, algorithms=["HS256"], options={"verify_signature": False})

        return user_data['id']

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
        await User(
            chat_id=self.event.chat.id,
            accessToken=rpc_response.accessToken,
            cookies=response.cookies
        ).save()

        return rpc_response

    # categories -------------------------------------------------------------------------------------------------------
    async def get_categories(self, chat_id: int, parent_id: int = None) -> GetCategoriesResponse:
        user_id = await self.__get_user_id(chat_id)
        rpc_response = await self.__request(
            method="get",
            url="/categories",
            request_obj=GetCategoriesRequest(userID=user_id, parentID=parent_id),
            response_obj=GetCategoriesResponse
        )

        return rpc_response

    async def create_category(self, chat_id: int, name: str, parent_id: int = None) -> CreateCategoryResponse:
        user_id = await self.__get_user_id(chat_id)
        rpc_response = await self.__request(
            method="post",
            url="/categories",
            request_obj=CreateCategoryRequest(userID=user_id, name=name, parentID=parent_id),
            response_obj=CreateCategoryResponse
        )

        return rpc_response

    async def get_counterparties(self, chat_id: int) -> GetCounterpartiesResponse:
        user_id = await self.__get_user_id(chat_id)
        rpc_response = await self.__request(
            method="get",
            url="/counterparties",
            request_obj=GetCounterpartiesRequest(userID=user_id),
            response_obj=GetCounterpartiesResponse
        )

        return rpc_response
