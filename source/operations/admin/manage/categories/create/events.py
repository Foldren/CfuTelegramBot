from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from components.tools import Tool
from modules.gateway.api import ApiGateway
from modules.gateway.responses.auth import SignInResponse
from operations.not_authorized.messages import AuthorizationMessage


async def on_start_categories_dialog(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    message_r = AuthorizationMessage(message_text=message.text)
    redis = dialog_manager.middleware_data["redis"]
    auth_r = await ApiGateway(redis=redis, user_id=message.from_user.id).auth(message_r.email, message_r.password)
    processed_auth_r: SignInResponse = await Tool.handle_exceptions(auth_r, message, SignInResponse)

    dialog_manager.dialog_data['fio'] = processed_auth_r.user.fio

    await redis.user.set(
        chat_id=message.from_user.id,
        access_token=processed_auth_r.accessToken,
        fio=processed_auth_r.user.fio
    )

    await dialog_manager.done()
