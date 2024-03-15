from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd.select import ManagedMultiselect
from modules.gateway.subclasses.counterparty import ApiCounterparty
from states.counterparties import DeleteCounterpartiesStates


async def on_start_delete_counterparty(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    if 'show_distrib' in dialog_manager.dialog_data:
        if dialog_manager.dialog_data['show_distrib']:
            cps_show_mode = 'not_distributed'
        else:
            cps_show_mode = 'distributed'
    else:
        cps_show_mode = 'distributed'

    await dialog_manager.start(state=DeleteCounterpartiesStates.select_counterparties,
                               data={'cps_show_mode': cps_show_mode})


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
