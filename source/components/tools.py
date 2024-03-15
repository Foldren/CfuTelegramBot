from dataclasses import dataclass, asdict, fields
from typing import Union, Any
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from httpx import Response
from components.dataclasses import DialogCategory, DialogCounterparty
from components.text import Text
from modules.gateway.responses.children import DCategory, DCounterparty
from modules.gateway.responses.rpc import RpcResponse, RpcExceptionResponse
from modules.redis.models import User
from modules.redis.redis_om import RedisOM
from states.authorization import AuthorizationStates


class Tool:
    fsm: FSMContext
    d_manager: DialogManager

    def __init__(self, fsm: FSMContext = None, d_manager: DialogManager = None):
        self.fsm = fsm
        self.d_manager = d_manager

    @staticmethod
    async def get_last_queue_category(dialog_data: dict):
        return dialog_data['queue'][-1]['id'] if 'queue' in dialog_data else None

    @staticmethod
    async def get_dict_categories(categories: list[DCategory], extended_option: str = None):
        result = []
        for c in categories:
            match extended_option:
                case "status":
                    c_name = f"💤 {c.name}" if int(c.status) == 0 else c.name
                case "has_children":
                    c_name = f"🔹 {c.name}" if int(c.hasChildren) == 0 else c.name
                case _:
                    c_name = c.name
            d_category = DialogCategory(id=c.id, name=c_name, status=c.status, hasChildren=int(c.hasChildren))
            result.append(DialogCategory.to_dict(d_category))

        return result

    @staticmethod
    async def get_dict_counterparties(counterparties: list[DCounterparty]):
        result = []
        for c in counterparties:
            d_category = DialogCounterparty(id=c.id, inn=c.inn, name=c.name, categoryID=c.categoryID,
                                            categoryName=c.categoryName)
            result.append(DialogCounterparty.to_dict(d_category))

        return result

    @staticmethod
    async def get_item_from_dict(items: list[dict], param: str, value: Any, dataclass_obj: dataclass):
        double_obj = dataclass_obj
        for item in items:
            if item[param] == value:
                cls_fields = fields(double_obj)
                for field in cls_fields:
                    if field.name != "data":
                        setattr(double_obj, field.name, field.type(item[field.name]) if item[field.name] is not None
                        else None)

                return double_obj

    @staticmethod
    async def get_counterparties_show_mode(dialog_data: dict):
        if 'show_distrib' in dialog_data:
            if dialog_data['show_distrib']:
                cps_show_mode = 'not_distributed'
            else:
                cps_show_mode = 'distributed'
        else:
            cps_show_mode = 'distributed'

        return cps_show_mode

    @staticmethod
    async def handle_exceptions(response: Response, dm: DialogManager,
                                response_type: dataclass) -> Any:
        title = Text.title('Ошибка')
        msg_text = "\n⛔ "
        chat_id = await Tool.get_chat_id(dm.event)

        try:
            rpc_response = RpcResponse.from_dict(response.json())
            rpc_response.data = response_type.from_dict(rpc_response.data) if rpc_response.data is not None else None
        except AttributeError:
            rpc_response = RpcExceptionResponse.from_dict(response.json())

        if hasattr(rpc_response, "data"):
            if hasattr(rpc_response, "error"):
                if rpc_response.error is not None:
                    await dm.event.bot.send_message(chat_id=chat_id, text=title + msg_text + rpc_response.error.message)
                    # Если неверный логин пароль, начинаем диалог с авторизацией
                    if rpc_response.error.statusCode == 401:
                        redis_conn: RedisOM = dm.middleware_data['redis']
                        await redis_conn.delete(User, pk=chat_id)
                        await dm.start(state=AuthorizationStates.start, mode=StartMode.RESET_STACK)
                    raise CancelHandler(rpc_response.error.message)
                else:
                    return response_type.from_dict(rpc_response.data)
            else:
                return response_type.from_dict(rpc_response.data)
        else:
            for row in rpc_response.message:
                msg_text += row + ". "
            await dm.event.bot.send_message(chat_id=chat_id, text=title + msg_text)
            raise CancelHandler

    @staticmethod
    async def get_chat_id(event: Union[Message, CallbackQuery]) -> int:
        return event.from_user.id if hasattr(event, "data") else event.chat.id

    @staticmethod
    async def generate_param_url(start_url: str, params_name: str, params: list) -> str:
        return f"{start_url}?" + "&".join([f"{params_name}[{i}]={v}" for i, v in enumerate(params)])

    @staticmethod
    async def message_to_dataclass(message: Message, dataclass_obj: dataclass,
                                   is_list: bool = False, to_dict: bool = False):
        msg_list_data = message.text.split("\n")

        if is_list:
            dataclass_list_obj = []

            msg_element_list_data = []
            element_number = 1
            for param in msg_list_data:
                if (param == "") or (element_number == len(msg_list_data)):
                    if element_number == len(msg_list_data):
                        msg_element_list_data.append(param)
                    element_d_obj = dataclass_obj(*msg_element_list_data)
                    if to_dict:
                        dataclass_list_obj.append(asdict(element_d_obj))
                    else:
                        dataclass_list_obj.append(element_d_obj)
                    msg_element_list_data = []
                elif param != "":
                    msg_element_list_data.append(param)
                element_number += 1
            return dataclass_list_obj

        else:
            if to_dict:
                result_one_obj = asdict(dataclass_obj(*msg_list_data))
            else:
                result_one_obj = dataclass_obj(*msg_list_data)
            return result_one_obj

    @staticmethod
    async def callback_to_dataclass(callback: CallbackQuery, dataclass_obj: dataclass) -> dataclass:
        list_data = callback.data.split(":")

        # Убираем первый элемент
        list_data.pop(0)
        cls_fields = fields(dataclass_obj)

        i = 0
        for field in cls_fields:
            if field.name != "data":
                # Если пошли объекты без значений значит записываем дефолтные
                try:
                    setattr(dataclass_obj, field.name, field.type(list_data[i]))
                except IndexError:
                    setattr(dataclass_obj, field.name, field.default)
                i += 1

        return dataclass_obj
