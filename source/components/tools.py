from dataclasses import dataclass
from typing import Union, Any, Awaitable
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from components.text import Text
from modules.gateway.responses.rpc import RpcResponse, RpcExceptionResponse


class Tool:
    fsm: FSMContext
    d_manager: DialogManager

    def __init__(self, fsm: FSMContext = None, d_manager: DialogManager = None):
        self.fsm = fsm
        self.d_manager = d_manager

    @staticmethod
    async def handle_exceptions(rpc_response: Union[RpcResponse, RpcExceptionResponse], message: Message,
                                response_type: dataclass) -> Any:
        title = Text.title('Ошибка')
        msg_text = "\n⛔ "

        if hasattr(rpc_response, "data"):
            if hasattr(rpc_response, "error"):
                await message.answer(text=title + msg_text + rpc_response.error.message)
                raise CancelHandler
            else:
                return response_type.from_dict(rpc_response.data)
        else:
            for row in rpc_response.message:
                msg_text += row + ". "
            await message.answer(text=title + msg_text)
            raise CancelHandler

    @staticmethod
    async def get_scrolling_group_btns(list_names: list[str], list_id: list[str], on_click_func: Any) -> list[Button]:
        list_buttons = []
        for btn_id, name in list_id, list_names:
            list_buttons.append(Button(text=name, id=btn_id, on_click=on_click_func))

        return list_buttons


