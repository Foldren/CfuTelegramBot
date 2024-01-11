from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_dialog import DialogManager
from operations.admin.states import GetCategoriesLevelStates

rt = Router()
rt.message.filter(F.chat.type == "private")


@rt.message(F.text == "Категории")
async def get_categories(message: Message, dialog_manager: DialogManager, state: FSMContext):
    await dialog_manager.start(state=GetCategoriesLevelStates.render)
