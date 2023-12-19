from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from components.filters import IsNotAuthorizedFilter
from operations.not_authorized.states import AuthorizationStates

rt = Router()
rt.message.filter(IsNotAuthorizedFilter(), F.chat.type == "private")


@rt.message(F.text == "Авторизация", IsNotAuthorizedFilter())
async def authorization(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=AuthorizationStates.start, mode=StartMode.RESET_STACK)
