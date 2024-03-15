from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Start, Cancel, Row, ScrollingGroup, Select, Button, Toggle, Column
from aiogram_dialog.widgets.text import Const, Multi, Format
from events.counterparties.create import on_start_create_counterparty
from events.counterparties.delete import on_start_delete_counterparty
from events.counterparties.get import on_distribution_toggle_selected, on_select_counterparty
from events.counterparties.update import on_start_update_counterparty
from getters.counterparties import get_counterparties
from states.counterparties import GetCounterpartiesStates, DeleteCounterpartiesStates, UpdateCounterpartyStates


counterparties = Window(
    Multi(
        Const("<b>Контрагенты</b>"),
        Const("💼 Здесь вы можете настроить контрагентов вашего бота Управляйки."),
        Const(f"<u>Кнопки управления:</u>\n"
              f"➕ - добавить контрагента.\n"
              f"✏️ - редактировать контрагентов.\n"
              f"🗑 - удалить контрагентов.\n"
              f"⛔️ - отменить операцию."),
        Const(f"📥 <i>Также вы можете переключаться между (не) распределенными контрагентами, для распределения, "
              f"нажмите на нужный.</i>"),
        sep="\n\n"
    ),
    Toggle(
        text=Format("{item[name]}"),
        id="t_distribution",
        item_id_getter=lambda item: item['show_distrib'],
        items="distribution_toggle",
        on_click=on_distribution_toggle_selected,
    ),
    Row(
        Button(id="create_counterparty", text=Const("➕"), on_click=on_start_create_counterparty,
               when=~F['dialog_data']['show_distrib']),
        Button(id="update_counterparty", text=Const("✏️"), on_click=on_start_update_counterparty,
               when=F['there_are_counterparties']),
        Button(id="delete_counterparties", text=Const("🗑"), on_click=on_start_delete_counterparty,
               when=F['there_are_counterparties']),
        Cancel(text=Const("⛔️")),
    ),
    Button(text=Const("Нет ни одного контрагента"), id="no_contragents", when=~F['there_are_counterparties']),
    ScrollingGroup(
        Select(
            text=Format("{item[status]}{item[inn]} - {item[name]}"),
            items='counterparties',
            item_id_getter=lambda item: item['id'],
            on_click=on_select_counterparty,
            id="counterparty"
        ),
        id="counterparties_sc",
        width=1,
        height=4,
        hide_on_single_page=True,
    ),
    state=GetCounterpartiesStates.render,
    getter=get_counterparties
)
