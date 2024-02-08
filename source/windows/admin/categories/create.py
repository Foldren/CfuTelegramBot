from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Multi
from events.admin.categories.create import on_select_name
from states.categories import CreateCategoryStates


select_name = Window(
    Multi(
        Const(f"<b>Создание категории:</b> <i>(шаг 1)</i>"),
        Const(f"👉 Введите название новой категории.\n"
              f"<i>(статус категории по умолчаниию - активный)</i>"),
        sep="\n\n"
    ),
    Cancel(text=Const("Отмена ⛔️️")),
    MessageInput(func=on_select_name, content_types=[ContentType.TEXT]),
    state=CreateCategoryStates.select_name
)
