from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from operations.states import NotAuthorizationStates

rt = Router()

rt.message.filter(F.chat.type == "private")
rt.callback_query.filter(F.message.chat.type == "private")


@rt.callback_query(F.data == 'disabled')
async def disable_button(callback: CallbackQuery):
    await callback.answer()
    return


@rt.startup()
async def authorization(state: FSMContext):
    await state.set_state(NotAuthorizationStates.authorization)
