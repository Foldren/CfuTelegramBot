from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from components.dataclasses import AuthorizationMessage
from components.tools import Tool
from modules.gateway.api import ApiGateway
from modules.redis.models import User
from modules.redis.redis_om import RedisOM
from states.menu import MenuStates


async def on_authorization(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    try:
        message_r = await Tool.message_to_dataclass(message, AuthorizationMessage)
        response = await ApiGateway(dm=dialog_manager).auth(message_r.email, message_r.password)

        if response.user.role == "Admin":
            dialog_manager.dialog_data['fio'] = response.user.fio

            await dialog_manager.next()
            await dialog_manager.show(show_mode=ShowMode.DELETE_AND_SEND)
            await dialog_manager.start(state=MenuStates.main, mode=StartMode.RESET_STACK)
        else:
            redis_conn: RedisOM = dialog_manager.middleware_data['redis']
            await redis_conn.delete(User, pk=message.chat.id)
            await message.answer("⛔️ Бот пока работает только с админами")

    except TypeError:
        await message.answer("⛔️ Укажите пароль с новой строки.")


