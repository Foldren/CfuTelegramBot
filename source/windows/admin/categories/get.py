from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Start, Cancel, Row, ScrollingGroup, Select, Button
from aiogram_dialog.widgets.text import Const, Multi, Format
from components.getters import gtr_get_main_categories
from events.admin.categories.create import on_start_create
from events.admin.categories.delete import on_start_delete
from events.admin.categories.get import on_get_parents, on_get_children
from events.admin.categories.update import on_start_update
from states.categories import GetCategoriesStates, DeleteCategoriesStates, CreateCategoryStates, UpdateCategoryStates


main_categories = Window(
    Multi(
        Const("<b>Категории</b>"),
        Const("📋 Здесь вы можете настроить категории доходов и расходов на разных уровнях "
              "вложенности, для последующего внесения их в вашу гугл таблицу."),
        Const(f"<u>Кнопки управления:</u>\n"
              f"➕ - добавить категорию на уровень.\n"
              f"✏️ - редактировать категории.\n"
              f"❌️ - удалить категории.\n"
              f"⛔️ - отменить операцию.",
              when=F['there_are_categories']),
        Const(f"<u>Кнопка управления:</u>\n"
              f"➕ - добавить категорию на уровень.\n"
              f"⛔️ - отменить операцию.",
              when=~F['there_are_categories']),
        Const("<i>👉 Для перехода на уровень ниже, нажмите на нужную категорию.</i>"),
        sep="\n\n"
    ),
    Row(
        Button(id="create_category", text=Const("➕"), on_click=on_start_create),
        Button(id="update_category", text=Const("✏️"), on_click=on_start_update, when=F['there_are_categories']),
        Button(id="delete_categories", text=Const("❌"), on_click=on_start_delete, when=F['there_are_categories']),
        Cancel(text=Const("⛔️"))
    ),
    ScrollingGroup(
        Select(
            text=Format("{item[2]}{item[1]}"),
            items='categories',
            item_id_getter=lambda i: str(i[0]) + ":" + str(i[1]),
            on_click=on_get_children,
            id="categories_s"
        ),
        id="categories_sc",
        width=2,
        height=3,
        hide_on_single_page=True,
    ),
    state=GetCategoriesStates.render_main,
    getter=gtr_get_main_categories
)

child_categories = Window(
    Multi(
        Const("<b>Категории</b>"),
        Format("<u>Вложенность</u>: <b>{dialog_data[queue_frmt]}</b>"),
        sep="\n\n"
    ),
    Row(
        Button(id="back_to_parent_categories", text=Const("⬅️"), on_click=on_get_parents),
        Button(id="create_category", text=Const("➕"), on_click=on_start_create),
        Button(id="update_category", text=Const("✏️"), on_click=on_start_update,
               when=F['dialog_data']['there_are_categories']),
        Button(id="delete_categories", text=Const("❌"), on_click=on_start_delete,
               when=F['dialog_data']['there_are_categories']),
        Cancel(text=Const("⛔️"))
    ),
    ScrollingGroup(
        Select(
            text=Format("{item[2]}{item[0]}"),
            items=F['dialog_data']['categories'],
            item_id_getter=lambda i: str(i[0]) + ":" + str(i[1]),
            on_click=on_get_children,
            id="categories_s"
        ),
        id="categories_sc",
        width=2,
        height=3,
        hide_on_single_page=True,
    ),
    state=GetCategoriesStates.render_child
)
