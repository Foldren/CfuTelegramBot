from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog.widgets.text import Const
from components.filters import IsNotAuthorizedFilter
from operations.not_authorized.messages import AuthorizationMessage
from operations.not_authorized.states import AuthorizationStates
from operations.states import NotAuthorizationStates
from modules.gateway.api import ApiGateway
from source.operations.not_authorized.authorization import texts

rt = Router()
rt.message.filter(IsNotAuthorizedFilter(), F.chat.type == "private")


@rt.message(NotAuthorizationStates.authorization)
async def send_data(message: Message, state: FSMContext):
    await state.set_state(AuthorizationStates.start)
    await message.answer(text=await texts.send_data())


@rt.message(AuthorizationStates.start)
async def authorization(message: Message, state: FSMContext):
    message_r = AuthorizationMessage(message_text=message.text)
    auth_r = await ApiGateway().auth(message_r.email, message_r.password)
    await message.answer(text=await texts.authorization(auth_r.data.user.fio))
    await state.clear()
