from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd.select import ManagedMultiselect

from modules.gateway.subclasses.category import ApiCategory
from states.categories import DeleteCategoriesStates


async def on_start_delete(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    parent_id = dialog_manager.dialog_data['parent_id']
    await dialog_manager.start(state=DeleteCategoriesStates.select_categories, data={'parent_id': parent_id})


async def on_select_categories(event: CallbackQuery, select: ManagedMultiselect, dialog_manager: DialogManager,
                               category: str):
    dialog_manager.dialog_data['selected_categories'] = select.get_checked()
    dialog_manager.dialog_data['are_selected'] = True if dialog_manager.dialog_data['selected_categories'] else False


async def on_save(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    del_categories_id = [int(x) for x in dialog_manager.dialog_data['selected_categories']]
    api_gw = ApiCategory(event=callback)
    await api_gw.delete(categories_id=del_categories_id)
    await callback.answer("✅ Категории удалены успешно.", show_alert=True)
    await dialog_manager.done()
