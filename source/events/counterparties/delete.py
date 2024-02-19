from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd.select import ManagedMultiselect
from modules.gateway.subclasses.counterparty import ApiCounterparty


async def on_select_counterparties(event: CallbackQuery, select: ManagedMultiselect, dialog_manager: DialogManager,
                                   counterparty_id: str):
    dialog_manager.dialog_data['selected_counterparties'] = select.get_checked()
    dialog_manager.dialog_data['are_selected'] = True if dialog_manager.dialog_data['selected_counterparties'] \
        else False


async def on_save(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    del_counterparties_id = [int(x) for x in dialog_manager.dialog_data['selected_counterparties']]

    await ApiCounterparty(dm=dialog_manager).delete(counterparties_id=del_counterparties_id)
    await callback.answer("✅ Контрагенты удалены успешно.", show_alert=True)
    await dialog_manager.done()
