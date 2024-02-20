from dataclasses import asdict, dataclass
from typing import Any
import jwt
from aiogram_dialog import DialogManager
from httpx import AsyncClient
from jwt import ExpiredSignatureError
from components.tools import Tool
from config import GATEWAY_PATH, JWT_SECRET, UA_TELEGRAM
from modules.gateway.requests.auth import SignInRequest
from modules.gateway.responses.auth import SignInResponse, RefreshResponse
from modules.redis.models import User
from modules.redis.redis_om import RedisOM


class ApiGateway:
    main_path: str = GATEWAY_PATH
    headers = {"User-Agent": UA_TELEGRAM}
    dm: DialogManager

    def __init__(self, dm: DialogManager):
        """
        При инициализации передаем event
        :param dm: объект dialog_manager
        """
        self.dm = dm

    async def __refresh(self):
        chat_id = await Tool.get_chat_id(self.dm.event)
        message = await self.dm.event.bot.send_message(chat_id, "Обновление данных авторизации 🔄")
        redis_conn: RedisOM = self.dm.middleware_data['redis']
        user: User = await redis_conn.get(User, pk=chat_id)

        self.headers.pop('Authorization')

        async with AsyncClient(verify=True) as async_session:
            response_token = await async_session.post(
                url=self.main_path + "/auth/refresh",
                headers=self.headers,
                cookies=user.cookies
            )

            refresh_response = await Tool.handle_exceptions(response_token, self.dm, RefreshResponse)

            # Обновляем access_token
            access_token = refresh_response.accessToken
            self.headers['Authorization'] = 'Bearer ' + access_token

            user.accessToken = access_token
            user.cookies = {'refresh': response_token.cookies['refresh']}
            await redis_conn.save(user)

        await message.delete()

    async def _request(self, method: str, url: str, response_obj, request_obj: dataclass = None,
                       data_in_url: bool = False) -> Any:
        # Прикрепляем текущий токен
        chat_id = await Tool.get_chat_id(event=self.dm.event)
        redis_conn: RedisOM = self.dm.middleware_data['redis']
        user: User = await redis_conn.get(User, pk=chat_id)

        try:
            # Преобразуем объект данных в dict, удаляем пустые значения
            dict_params = asdict(request_obj, dict_factory=lambda x: {k: v for (k, v) in x if v is not None})
            # Cтавим условия на установку параметров в зависимости от метода
            json_data = dict_params if (method == "post" or method == "patch") and not data_in_url else None
            params_data = dict_params if (method == "get" or method == "delete") and not data_in_url else None

        # Если параметры указаны в строке то указываем их в None
        except TypeError:
            json_data = None
            params_data = None

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
                # Обновляем токен в случае истечения срока действия
                await self.__refresh()

                # Снова выполняем запрос
                response = await async_session.request(
                    method=method,
                    url=self.main_path + url,
                    json=json_data,
                    params=params_data,
                )

            # Проверяем на ошибки
            rpc_response = await Tool.handle_exceptions(response, self.dm, response_obj)

        return rpc_response

    async def auth(self, email: str, password: str) -> SignInResponse:
        async with AsyncClient(verify=False) as async_session:
            response = await async_session.post(
                url=self.main_path + "/auth/sign-in",
                headers=self.headers,
                json=asdict(SignInRequest(email, password)),
            )

        rpc_response = await Tool.handle_exceptions(response, self.dm, SignInResponse)

        # Сохраняем токен
        self.headers['Authorization'] = 'Bearer ' + rpc_response.accessToken

        # Записываем данные
        redis_conn: RedisOM = self.dm.middleware_data['redis']

        user = User(pk=self.dm.event.chat.id,
                    accessToken=rpc_response.accessToken,
                    role=rpc_response.user.role,
                    cookies={'refresh': response.cookies['refresh']}
                    )

        await redis_conn.save(user)

        return rpc_response
