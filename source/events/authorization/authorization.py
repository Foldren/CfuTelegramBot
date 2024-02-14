from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from components.messages_responses import AuthorizationMessage
from components.tools import Tool
from modules.gateway.api import ApiGateway
from modules.redis.models import User
from states.menu import MenuStates


async def on_authorization(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    message_r = await Tool.message_to_dataclass(message, AuthorizationMessage)
    response = await ApiGateway(event=dialog_manager.event).auth(message_r.email, message_r.password)

    if response.user.role == "Admin":
        dialog_manager.dialog_data['fio'] = response.user.fio

        await dialog_manager.next()
        await dialog_manager.show(show_mode=ShowMode.DELETE_AND_SEND)
        await dialog_manager.start(state=MenuStates.main, mode=StartMode.RESET_STACK)
    else:
        await User.find(User.chat_id == message.chat.id).delete()
        await message.answer("⛔️ Бот пока работает только с админами")
