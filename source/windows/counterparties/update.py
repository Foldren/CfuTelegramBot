from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select, Button, Row, SwitchTo, Group
from aiogram_dialog.widgets.text import Const, Multi, Format
from components.text import Text
from events.counterparties.update import on_select_counterparty, on_back_to_counterparties, on_update_name, \
    on_update_inn, on_get_child_categories, on_get_parent_categories
from getters.counterparties import get_counterparties, get_selected_counterparty, get_attach_categories
from states.counterparties import UpdateCounterpartyStates


select_counterparty = Window(
    Multi(
        Const(Text.title("Редактирование контрагента", 1, with_step=True)),
        Const("👉 Выберите контрагента, параметры которого хотите изменить."),
        sep="\n\n"
    ),
    Cancel(text=Const("Отмена ⛔️")),
    ScrollingGroup(
        Select(
            text=Format("{item[inn]} - {item[name]}"),
            items='counterparties',
            item_id_getter=lambda item: item['id'],
            on_click=on_select_counterparty,
            id="counterparties_s"
        ),
        id="counterparties_sc",
        width=1,
        height=4,
        hide_on_single_page=True,
    ),
    state=UpdateCounterpartyStates.select_counterparty,
    getter=get_counterparties
)

select_counterparty_param = Window(
    Multi(
        Const(Text.title("Редактирование контрагента", 2, with_step=True)),
        Const("👉 Выберите параметр, который хотите изменить у контрагента."),
        Format("<u>Данные выбранного контрагента:</u>\n"
               "<b>Наименование</b> - {selected_counterparty[name]}.\n"
               "<b>ИНН</b> - {selected_counterparty[inn]}.\n"
               "<b>Категория распределения</b> - {selected_counterparty[categoryName]}."),
        sep="\n\n"
    ),
    Button(text=Const("Назад в меню ⬅️"), on_click=on_back_to_counterparties, id="back_to_counterparties_list"),
    Group(
        SwitchTo(text=Const("Наименование"), id="update_counterparty_name",
                 state=UpdateCounterpartyStates.update_name),
        SwitchTo(text=Const("ИНН"), id="update_counterparty_inn",
                 state=UpdateCounterpartyStates.update_inn),
        SwitchTo(text=Const("Категория распределения"), id="update_counterparty_category",
                 state=UpdateCounterpartyStates.attach_new_category),
        width=2
    ),
    state=UpdateCounterpartyStates.select_param,
    getter=get_selected_counterparty
)

update_counterparty_name = Window(
    Multi(
        Const(Text.title("Редактирование контрагента", 3, with_step=True)),
        Const(f"👉 Введите новое имя для контрагента."),
        sep="\n\n"
    ),
    Cancel(text=Const("Отмена ⛔️")),
    MessageInput(func=on_update_name, content_types=[ContentType.TEXT]),
    state=UpdateCounterpartyStates.update_name
)

update_counterparty_inn = Window(
    Multi(
        Const(Text.title("Редактирование контрагента", 3, with_step=True)),
        Const(f"👉 Введите новый ИНН для контрагента."),
        sep="\n\n"
    ),
    Cancel(text=Const("Отмена ⛔️")),
    MessageInput(func=on_update_inn, content_types=[ContentType.TEXT]),
    state=UpdateCounterpartyStates.update_inn
)

attach_new_category = Window(
    Multi(
        Const(Text.title("Редактирование контрагента", 3, True)),
        Const(f"🗂 Выберите для контрагента новую категорию распределения.\n"
              f"<i>(доступные для прикрепления категории отмечены эмодзи - 🔹)</i>"),
        sep="\n\n"
    ),
    Row(
        Button(id="back_to_parent_categories", text=Const("⬅️"), on_click=on_get_parent_categories,
               when=F['is_child_categories']),
        Cancel(text=Const("Отмена ⛔️"))
    ),
    ScrollingGroup(
        Select(
            text=Format("{item[name]}"),
            items='categories',
            item_id_getter=lambda item: item['id'],
            on_click=on_get_child_categories,
            id="attach_new_category"
        ),
        id="categories_sc",
        width=2,
        height=3,
        hide_on_single_page=True,
    ),
    state=UpdateCounterpartyStates.attach_new_category,
    getter=get_attach_categories
)
