from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, Button
from components.callbacks_responses import GetCategoriesCallback
from components.tools import Tool
from modules.gateway.responses.category import GetCategoriesResponse
from modules.gateway.subclasses.category import ApiCategory
from states.categories import UpdateCategoryStates


async def on_start_update(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    # parent_id это либо последний элемент очереди, либо None, все просто
    parent_id = await Tool.get_last_queue_category(dialog_manager.dialog_data)
    await dialog_manager.start(state=UpdateCategoryStates.select_category, data={'parent_id': parent_id})


async def on_select_category(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, str_item: str):
    category: GetCategoriesCallback = await Tool.callback_to_dataclass(callback, GetCategoriesCallback)
    dialog_manager.dialog_data['selected_category'] = {"id": category.id,
                                                       "name": category.name,
                                                       "status": category.status}

    # Записываем F['selected_category']['status'] для окна
    dialog_manager.dialog_data['selected_category']['status'] = False if category.status == 0 else True

    await dialog_manager.next()


async def on_update_status(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    category_id = dialog_manager.dialog_data['selected_category']['id']
    status = False if widget.widget_id == "cs_active" else True

    # Обновляем статус
    dialog_manager.dialog_data['selected_category']['status'] = status

    await ApiCategory(event=callback).update(category_id=category_id, status=int(status))
    await dialog_manager.show(show_mode=ShowMode.EDIT)


async def on_update_name(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    category = dialog_manager.dialog_data['selected_category']
    api_c = ApiCategory(event=message)
    parent_id = dialog_manager.start_data['parent_id']

    # Обновляем категорию и получаем обновленный список
    await api_c.update(category_id=category['id'], name=message.text)
    categories_r = await api_c.get(parent_id=parent_id)

    categories_frmt = await Tool.get_categories_frmt(categories_r.categories, "status")

    await message.answer("Название категориии изменено успешно ✅")
    await dialog_manager.done()
    await dialog_manager.update(data={'categories': categories_frmt}, show_mode=ShowMode.EDIT)


async def on_back_to_categories(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    categories_r: GetCategoriesResponse = await ApiCategory(event=callback).get(
        parent_id=dialog_manager.start_data['parent_id'])
    categories = categories_r.categories

    await dialog_manager.done()
    await dialog_manager.update(data={
        "categories": await Tool.get_categories_frmt(categories, "status"),
    }, show_mode=ShowMode.EDIT)

