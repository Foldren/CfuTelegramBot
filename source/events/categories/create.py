from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from components.tools import Tool
from modules.gateway.subclasses.category import ApiCategory
from states.categories import CreateCategoryStates


async def on_start_create(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    # parent_id это либо последний элемент очереди, либо None, все просто
    parent_id = await Tool.get_last_queue_category(dialog_manager.dialog_data)
    await dialog_manager.start(state=CreateCategoryStates.select_name, data={'parent_id': parent_id})


async def on_select_name(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    item_id = dialog_manager.start_data['parent_id']
    api_c = ApiCategory(event=message)

    # Создаем категорию
    await ApiCategory(event=message).create(parent_id=item_id, name=message.text)

    # Получаем новый список категорий
    categories_r = await api_c.get(parent_id=item_id)

    await message.answer("Категория успешно добавлена в систему ✅")
    await dialog_manager.done()
    await dialog_manager.update(data={
        'categories': await Tool.get_categories_frmt(categories_r.categories, "status"),
        "there_are_categories": True,
    }, show_mode=ShowMode.EDIT)
