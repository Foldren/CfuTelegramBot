from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const
from events.admin.categories.create import on_select_name
from states.categories import CreateCategoryStates


select_name = Window(
    Const(f"👉 Введите название новой категории."),
    Cancel(text=Const("⛔️")),
    MessageInput(func=on_select_name, content_types=[ContentType.TEXT]),
    state=CreateCategoryStates.select_name
)
