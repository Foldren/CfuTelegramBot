from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, Button
from components.dataclasses import DialogCategory
from components.decorators import get_wselect_item
from components.tools import Tool
from modules.gateway.subclasses.category import ApiCategory
from states.categories import UpdateCategoryStates


async def on_start_update(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    # parent_id это либо последний элемент очереди, либо None, все просто
    parent_id = await Tool.get_last_queue_category(dialog_manager.dialog_data)
    await dialog_manager.start(state=UpdateCategoryStates.select_category, data={'parent_id': parent_id})


@get_wselect_item(data_cls=DialogCategory, items_name='d_categories')
async def on_select_category(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                             selected_category: DialogCategory):
    dialog_manager.dialog_data['selected_category'] = DialogCategory.to_dict(selected_category)

    # Записываем F['selected_category']['status'] для окна
    dialog_manager.dialog_data['selected_category']['status'] = False if selected_category.status == 0 else True
    await dialog_manager.next()


async def on_update_status(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    category = DialogCategory.from_dict(dialog_manager.dialog_data['selected_category'])
    status = False if widget.widget_id == "cs_active" else True
    api_c = ApiCategory(dm=dialog_manager)
    name_c = dialog_manager.dialog_data['selected_category']['name'].replace("💤 ", "")

    # Обновляем статус
    dialog_manager.dialog_data['selected_category']['status'] = status
    dialog_manager.dialog_data['selected_category']['name'] = name_c if status else f"💤 {name_c}"

    await api_c.update(category_id=category.id, status=int(status))
    await dialog_manager.show(show_mode=ShowMode.EDIT)


async def on_update_name(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    category = DialogCategory.from_dict(dialog_manager.dialog_data['selected_category'])
    api_c = ApiCategory(dm=dialog_manager)
    parent_id = dialog_manager.start_data['parent_id']
    new_c_name = message.text

    # Обновляем категорию и получаем обновленный список
    await api_c.update(category_id=category.id, name=new_c_name)

    categories = await api_c.get(parent_id=parent_id)

    await message.answer("Название категории изменено успешно ✅")
    dialog_manager.dialog_data['d_categories'] = await Tool.get_dict_categories(categories, "status")
    status = False if widget.widget_id == "cs_active" else True
    dialog_manager.dialog_data['selected_category']['name'] = new_c_name if status else f"💤 {new_c_name}"
    await dialog_manager.switch_to(show_mode=ShowMode.DELETE_AND_SEND, state=UpdateCategoryStates.select_param)


async def on_back_to_categories(callback: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    categories = await ApiCategory(dm=dialog_manager).get(parent_id=dialog_manager.start_data['parent_id'])
    await dialog_manager.done()
    dialog_manager.dialog_data['d_categories'] = await Tool.get_dict_categories(categories, "status")
    await dialog_manager.show(show_mode=ShowMode.EDIT)

