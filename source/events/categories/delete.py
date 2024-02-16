from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd.select import ManagedMultiselect
from components.tools import Tool
from modules.gateway.subclasses.category import ApiCategory
from states.categories import DeleteCategoriesStates


async def on_start_delete(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    # parent_id это либо последний элемент очереди, либо None, все просто
    parent_id = await Tool.get_last_queue_category(dialog_manager.dialog_data)
    await dialog_manager.start(state=DeleteCategoriesStates.select_categories, data={'parent_id': parent_id})


async def on_select_categories(event: CallbackQuery, select: ManagedMultiselect, dialog_manager: DialogManager,
                               category_id: str):
    dialog_manager.dialog_data['selected_categories'] = select.get_checked()
    dialog_manager.dialog_data['are_selected'] = True if dialog_manager.dialog_data['selected_categories'] else False


async def on_save(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    del_categories_id = [int(x) for x in dialog_manager.dialog_data['selected_categories']]
    api_c = ApiCategory(event=callback)
    parent_id = dialog_manager.start_data['parent_id']

    await api_c.delete(categories_id=del_categories_id)

    categories = await api_c.get(parent_id=parent_id)
    categories = await Tool.get_dict_categories(categories, "status")

    await callback.answer("✅ Категории удалены успешно.", show_alert=True)
    await dialog_manager.done()

    dialog_manager.dialog_data['d_categories'] = categories
    await dialog_manager.show(show_mode=ShowMode.EDIT)


