from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, Button
from components.callbacks_responses import GetCategoriesUpdateCallback
from components.tools import Tool
from modules.gateway.subclasses.category import ApiCategory
from states.categories import UpdateCategoryStates


async def on_start_update(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    parent_id = dialog_manager.dialog_data['parent_id']
    await dialog_manager.start(state=UpdateCategoryStates.select_category, data={'parent_id': parent_id})


async def on_select_category(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, str_item: str):
    category: GetCategoriesUpdateCallback = await Tool.callback_to_dataclass(callback, GetCategoriesUpdateCallback)
    dialog_manager.dialog_data['selected_category'] = {"id": category.id,
                                                       "name": category.name,
                                                       "status": category.status}
    await dialog_manager.next()


async def on_update_status(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    api_gw = ApiCategory(event=callback)
    category_id = dialog_manager.dialog_data['selected_category']['id']
    status = 0 if widget.widget_id == "cs_active" else 1

    dialog_manager.dialog_data['selected_category']['status'] = status

    await api_gw.update(category_id=category_id, status=status)
    await dialog_manager.show(show_mode=ShowMode.EDIT)


async def on_update_name(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    category = dialog_manager.dialog_data['selected_category']

    api_gw = ApiCategory(event=message)
    await api_gw.update(category_id=category['id'], name=message.text)

    await message.answer("Название категориии изменено успешно ✅")
    await dialog_manager.done()

