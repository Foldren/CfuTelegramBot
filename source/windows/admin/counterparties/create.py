from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Multi
from components.text import Text
from events.admin.categories.create import on_select_name
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
    MessageInput(func=on_select_name, content_types=[ContentType.TEXT]),
    state=CreateCounterpartyStates.write_params
)

select_category = Window(
    Multi(
        Const(Text.title("Создание контрагента", 2, True)),
        Const(f"🗂 Выберите категорию, к которой нужно прикрепить этого контрагента."),
        Const(f"<u>Список категорий с выстроенными очередями:</u>\n"
              f"<i>(соотнесите категорию по номеру в кнопке)</i>\n"),
        sep="\n\n"
    ),
    Cancel(text=Const("Отмена ⛔️️")),
    state=CreateCounterpartyStates.write_params
)
