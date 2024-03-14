from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Select
from components.dataclasses import DialogCounterparty
from components.decorators import get_wselect_item
from components.tools import Tool
from modules.gateway.subclasses.category import ApiCategory
from states.counterparties import UpdateCounterpartyStates


async def on_distribution_toggle_selected(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager,
                                          show_distrib: str):
    if show_distrib == 'True':
        dialog_manager.dialog_data['show_distrib'] = True
    else:
        dialog_manager.dialog_data['show_distrib'] = False

    await dialog_manager.show()


@get_wselect_item(data_cls=DialogCounterparty, items_name='d_counterparties')
async def on_select_counterparty(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                                 selected_counterparty: DialogCounterparty):
    if 'show_distrib' in dialog_manager.dialog_data:
        if dialog_manager.dialog_data['show_distrib']:
            await dialog_manager.start(state=UpdateCounterpartyStates.attach_new_category, show_mode=ShowMode.NO_UPDATE)

            # Формируем начальный список категорий (главных) доступных для прикрепления
            categories = await ApiCategory(dm=dialog_manager).get(parent_id=None, include_static=True)

            dialog_manager.dialog_data.update({
                "is_child_categories": False,
                'selected_counterparty': DialogCounterparty.to_dict(selected_counterparty),
                'd_categories': await Tool.get_dict_categories(categories, "has_children")
            })

            await dialog_manager.show(show_mode=ShowMode.EDIT)
            return

    await callback.answer()
