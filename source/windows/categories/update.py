from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select, Button, Next, Row, SwitchTo
from aiogram_dialog.widgets.text import Const, Multi, Format
from getters.categories import get_for_update_or_delete, get_selected_category
from events.categories.update import on_select_category, on_update_status, on_update_name, on_back_to_categories
from states.categories import UpdateCategoryStates


select_category = Window(
    Multi(
        Const("<b>Редактирование категории:</b> <i>(шаг 1)</i>"),
        Const("👉 Выберите категорию, параметры которой хотите изменить."),
        sep="\n\n"
    ),
    Cancel(text=Const("Отмена ⛔️")),
    ScrollingGroup(
        Select(
            text=Format("{item[name]}"),
            items='categories',
            item_id_getter=lambda item: item['id'],
            on_click=on_select_category,
            id="update_category"
        ),
        id="categories_sc",
        width=2,
        height=3,
        hide_on_single_page=True,
    ),
    state=UpdateCategoryStates.select_category,
    getter=get_for_update_or_delete
)

select_category_param = Window(
    Multi(
        Const("<b>Редактирование категории:</b> <i>(шаг 2)</i>"),
        Const("👉 Выберите параметр, который хотите изменить в этой категории."),
        Format("<u>Выбранная категория:</u> <b>{selected_category[name]}</b>"),
        sep="\n\n"
    ),
    Button(text=Const("Назад в меню ⬅️"), on_click=on_back_to_categories, id="back_to_categories_list"),
    Row(
        SwitchTo(text=Const("Название"), state=UpdateCategoryStates.update_name, id="update_c_name"),
        Button(text=Const("Статус: Активный ✅"), on_click=on_update_status,
               when=F['selected_category']['status'], id="cs_active"),
        Button(text=Const("Статус: Скрытый 💤"), on_click=on_update_status,
               when=~F['selected_category']['status'], id="cs_hidden"),
    ),
    state=UpdateCategoryStates.select_param,
    getter=get_selected_category
)

update_category_name = Window(
    Multi(
        Const(f"<b>Редактирование категории:</b> <i>(шаг 3)</i>"),
        Const(f"👉 Введите новое имя для категории."),
        sep="\n\n"
    ),
    Cancel(text=Const("Отмена ⛔️")),
    MessageInput(func=on_update_name, content_types=[ContentType.TEXT]),
    state=UpdateCategoryStates.update_name
)
