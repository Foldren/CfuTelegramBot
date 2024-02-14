from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select, Button, Row
from aiogram_dialog.widgets.text import Const, Multi, Format
from components.text import Text
from events.counterparties.create import on_get_parent_categories, on_get_child_categories, on_write_params
from getters.counterparties import get_attach_categories
from states.counterparties import CreateCounterpartyStates

write_params = Window(
    Multi(
        Const(Text.title("Создание контрагента", 1, True)),
        Const(f"<u>Введите данные контрагента:</u>\n"
              f"<b>ИНН</b> - в формате числа.\n"
              f"<b>Наименование</b> - в формате строки."),
        Const(Text.example("120400301202", "ООО Открытие")),
        sep="\n\n"
    ),
    Cancel(text=Const("Отмена ⛔️️")),
    MessageInput(func=on_write_params, content_types=[ContentType.TEXT]),
    state=CreateCounterpartyStates.write_params
)

select_attach_category = Window(
    Multi(
        Const(Text.title("Создание контрагента", 2, True)),
        Const(f"🗂 Выберите категорию, к которой нужно прикрепить этого контрагента.\n"
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
            text=Format("{item[1]}"),
            items='categories',
            item_id_getter=lambda item: f"{item[0]}:{item[1]}",
            on_click=on_get_child_categories,
            id="categories_s"
        ),
        id="categories_sc",
        width=2,
        height=3,
        hide_on_single_page=True,
    ),
    state=CreateCounterpartyStates.select_category,
    getter=get_attach_categories
)
