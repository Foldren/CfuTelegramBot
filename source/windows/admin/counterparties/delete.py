from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Row, Multiselect, Button
from aiogram_dialog.widgets.text import Const, Multi, Format
from components.getters import gtr_get_categories_for_update_and_delete
from events.admin.categories.delete import on_select_categories, on_save
from states.categories import DeleteCategoriesStates


select_categories = Window(
    Multi(
        Const("<b>Удаление категорий:</b> <i>(шаг 1)</i>"),
        Const("👉 Отметьте категории, которые нужно удалить."),
        Const("<i>⚠️ Важно: при удалении, исчезнут все вложенные подкатегории а также "
              "прикрепленные контрагенты!</i>"),
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
            items='categories',
            item_id_getter=lambda i: str(i[0]),
            on_state_changed=on_select_categories,
            id="categories_s"
        ),
        id="categories_sc",
        width=2,
        height=3,
        hide_on_single_page=True,
    ),
    state=DeleteCategoriesStates.select_categories,
    getter=gtr_get_categories_for_update_and_delete
)
