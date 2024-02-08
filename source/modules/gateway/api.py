from asyncio import sleep
from dataclasses import asdict, dataclass
from typing import Union, Any
import jwt
from aiogram.types import Message, CallbackQuery
from fake_useragent import UserAgent
from httpx import AsyncClient
from jwt import ExpiredSignatureError
from components.tools import Tool
from modules.gateway.responses.auth import SignInResponse, RefreshResponse
from modules.redis.models import User
from source.config import GATEWAY_PATH, JWT_SECRET
from source.modules.gateway.requests.auth import SignInRequest


class ApiGateway:
    main_path: str = GATEWAY_PATH
    headers = {"User-Agent": UserAgent().chrome}
    event: Union[Message, CallbackQuery]

    def __init__(self, event: Union[Message, CallbackQuery]):
        """
        При инициализации передаем event
        :param event: объект колбека или сообщения
        """
        self.event = event

    async def __refresh(self):
        chat_id = await Tool.get_chat_id(self.event)
        message = await self.event.bot.send_message(chat_id, "Обновление данных авторизации 🔄")
        user = await User.find(User.chat_id == chat_id).first()

        self.headers.pop('Authorization')

        async with AsyncClient(verify=True) as async_session:
            response_token = await async_session.post(
                url=self.main_path + "/auth/refresh",
                headers=self.headers,
                cookies=user.cookies
            )

            print(response_token)
            refresh_response = await Tool.handle_exceptions(response_token, self.event, RefreshResponse)

            # Обновляем access_token
            access_token = refresh_response.accessToken
            self.headers['Authorization'] = 'Bearer ' + access_token

            user.accessToken = access_token
            user.cookies = {'refresh': response_token.cookies['refresh']}
            await user.save()

        await message.delete()

    async def _request(self, method: str, url: str, request_obj: dataclass, response_obj,
                       data_in_url: bool = False) -> Any:
        # Прикрепляем текущий токен
        chat_id = await Tool.get_chat_id(event=self.event)
        user = await User.find(User.chat_id == chat_id).first()
        dict_params = asdict(request_obj, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
        json_data = dict_params if (method == "post" or method == "patch") and not data_in_url else None
        params_data = dict_params if (method == "get" or method == "delete") and not data_in_url else None

        self.headers['Authorization'] = 'Bearer ' + user.accessToken

        async with AsyncClient(verify=False, cookies=user.cookies, headers=self.headers) as async_session:
            # Пробуем выполнить запрос
            try:
                jwt.decode(user.accessToken, JWT_SECRET, algorithms=["HS256"])
                response = await async_session.request(
                    method=method,
                    url=self.main_path + url,
                    json=json_data,
                    params=params_data,
                )

            except ExpiredSignatureError:
                # Обновляем токен в случае задержки
                await self.__refresh()

                # Снова выполняем запрос
                response = await async_session.request(
                    method=method,
                    url=self.main_path + url,
                    json=json_data,
                    params=params_data,
                )

            # Проверяем на ошибки
            rpc_response = await Tool.handle_exceptions(response, self.event, response_obj)

        return rpc_response

    @staticmethod
    async def _get_user_id(chat_id: int):
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
