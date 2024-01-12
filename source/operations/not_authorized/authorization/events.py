from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from components.tools import Tool
from modules.gateway.api import ApiGateway
from modules.gateway.responses.auth import SignInResponse
from operations.admin.states import MenuStates
from operations.not_authorized.messages import AuthorizationMessage


async def on_authorization(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    message_r = AuthorizationMessage(message_text=message.text)
    redis = dialog_manager.middleware_data["redis"]
    response = await ApiGateway(redis=redis, event=dialog_manager.event).auth(message_r.email, message_r.password)

    dialog_manager.dialog_data['fio'] = response.user.fio

    await dialog_manager.next()
    await dialog_manager.show(show_mode=ShowMode.DELETE_AND_SEND)
    await dialog_manager.start(state=MenuStates.main, mode=StartMode.RESET_STACK)



