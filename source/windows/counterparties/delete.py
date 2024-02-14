from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Row, Multiselect, Button
from aiogram_dialog.widgets.text import Const, Multi, Format
from events.categories.delete import on_select_categories, on_save
from getters.counterparties import get_counterparties
from states.counterparties import DeleteCounterpartiesStates


select_counterparties = Window(
    Multi(
        Const("<b>Удаление контрагентов:</b> <i>(шаг 1)</i>"),
        Const("👉 Отметьте контрагентов, которые нужно удалить."),
        sep="\n\n"
    ),
    Row(
        Button(text=Const("Удалить выбранные 🗑"), on_click=on_save,
               id="save_btn", when=F['dialog_data']['are_selected']),
        Cancel(text=Const("Отмена ⛔️")),
    ),
    ScrollingGroup(
        Multiselect(
            checked_text=Format("☑️ {item[2]}{item[1]}"),
            unchecked_text=Format("{item[2]}{item[1]}"),
            items='counterparties',
            item_id_getter=lambda i: str(i[0]),
            on_state_changed=on_select_categories,
            id="counterparties_s"
        ),
        id="counterparties_sc",
        width=1,
        height=4,
        hide_on_single_page=True,
    ),
    state=DeleteCounterpartiesStates.select_counterparties,
    getter=get_counterparties
)
