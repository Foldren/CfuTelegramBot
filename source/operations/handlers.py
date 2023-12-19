from aiogram import Router, F
from aiogram.types import CallbackQuery

rt = Router()

rt.message.filter(F.chat.type == "private")
rt.callback_query.filter(F.message.chat.type == "private")


@rt.callback_query(F.data == 'disabled')
async def disable_button(callback: CallbackQuery):
    await callback.answer()
    return
