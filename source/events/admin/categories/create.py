from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from modules.gateway.subclasses.category import ApiCategory
from states.categories import CreateCategoryStates


async def on_start_create(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    parent_id = dialog_manager.dialog_data['parent_id']
    await dialog_manager.start(state=CreateCategoryStates.select_name, data={'parent_id': parent_id})


async def on_select_name(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    item_id = dialog_manager.start_data['parent_id']

    api_gw = ApiCategory(event=message)
    await api_gw.create(parent_id=item_id, name=message.text)

    await message.answer("Категория успешно добавлена в систему ✅")
    await dialog_manager.done()
