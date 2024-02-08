from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select, Button, Next, Row
from aiogram_dialog.widgets.text import Const, Multi, Format
from components.getters import gtr_get_categories_for_update
from events.admin.categories.update import on_select_category, on_update_status, on_update_name
from states.categories import UpdateCategoryStates


select_category = Window(
    Multi(
        Const("<b>Редактирование категории:</b> <i>(шаг 1)</i>"),
        Const("👉 Выберите категорию, которую хотите изменить."),
        sep="\n\n"
    ),
    Cancel(text=Const("⛔️")),
    ScrollingGroup(
        Select(
            text=Format("{item[2]}{item[1]}"),
            items='categories',
            item_id_getter=lambda i: str(i[0]) + ":" + str(i[1]) + ":" + str(i[3]),
            on_click=on_select_category,
            id="categories_s"
        ),
        id="categories_sc",
        width=2,
        height=3,
        hide_on_single_page=True,
    ),
    state=UpdateCategoryStates.select_category,
    getter=gtr_get_categories_for_update
)

select_param = Window(
    Multi(
        Const("<b>Редактирование категории:</b> <i>(шаг 2)</i>"),
        Const("👉 Выберите параметр, который хотите изменить в этой категории."),
        Format("<u>Выбранная категория:</u> <b>{dialog_data[selected_category][name]}</b>"),
        sep="\n\n"
    ),
    Cancel(text=Const("⛔️")),
    Row(
        Next(text=Const("Название")),
        Button(text=Const("Статус: Активный ✅"), on_click=on_update_status,
               when=F['dialog_data']['selected_category']['status'], id="cs_active"),
        Button(text=Const("Статус: Скрытый 💤"), on_click=on_update_status,
               when=~F['dialog_data']['selected_category']['status'], id="cs_hidden"),
    ),
    state=UpdateCategoryStates.select_param
)

update_name = Window(
    Multi(
        Const(f"<b>Редактирование категории:</b> <i>(шаг 3)</i>"),
        Const(f"👉 Введите новое имя для категории."),
        sep="\n\n"
    ),
    Cancel(text=Const("⛔️")),
    MessageInput(func=on_update_name, content_types=[ContentType.TEXT]),
    state=UpdateCategoryStates.update_name
)
