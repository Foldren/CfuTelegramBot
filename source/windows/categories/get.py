from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Row, ScrollingGroup, Select, Button
from aiogram_dialog.widgets.text import Const, Multi, Format
from getters.categories import get_main_ones, get_children
from events.categories.create import on_start_create
from events.categories.delete import on_start_delete
from events.categories.get import on_get_parents, on_get_children
from events.categories.update import on_start_update
from states.categories import GetCategoriesStates

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
            text=Format("{item[1]}"),  # Показываем название вместе со статусом
            items='categories',
            item_id_getter=lambda item: f"{item[0]}:{item[1]}",  # 0 - id, 1 - название
            on_click=on_get_children,
            id="categories_s"
        ),
        id="categories_sc",
        width=2,
        height=3,
        hide_on_single_page=True,
    ),
    state=GetCategoriesStates.render_main,
    getter=get_main_ones
)

child_categories = Window(
    Multi(
        Const("<b>Категории</b>"),
        Format("<u>Вложенность</u>: <b>{queue_frmt}</b>"),
        sep="\n\n"
    ),
    Row(
        Button(id="back_to_parent_categories", text=Const("⬅️"), on_click=on_get_parents),
        Button(id="create_category", text=Const("➕"), on_click=on_start_create),
        Button(id="update_category", text=Const("✏️"), on_click=on_start_update,
               when=F['there_are_categories']),
        Button(id="delete_categories", text=Const("❌"), on_click=on_start_delete,
               when=F['there_are_categories']),
        Cancel(text=Const("⛔️"))
    ),
    ScrollingGroup(
        Select(
            text=Format("{item[1]}"),  # Показываем название вместе со статусом
            items='categories',
            item_id_getter=lambda item: f"{item[0]}:{item[1]}",  # 0 - id, 1 - название
            on_click=on_get_children,
            id="categories_s"
        ),
        id="categories_sc",
        width=2,
        height=3,
        hide_on_single_page=True,
    ),
    state=GetCategoriesStates.render_child,
    getter=get_children
)
