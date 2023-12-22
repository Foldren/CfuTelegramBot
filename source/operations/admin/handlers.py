from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram_dialog import DialogManager, StartMode
from components.filters import IsNotAuthorizedFilter
from components.reply import keyb_markup_start_admin
from operations.not_authorized.states import AuthorizationStates

rt = Router()
rt.message.filter(F.chat.type == "private")


@rt.message(F.text == "Категории")
async def get_categories(message: Message, dialog_manager: DialogManager, state: FSMContext):
    dialog_manager.event.reply_markup = keyb_markup_start_admin

    await dialog_manager.start(state=AuthorizationStates.start, mode=StartMode.RESET_STACK)
