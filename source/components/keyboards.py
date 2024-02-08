from aiogram_dialog.widgets.kbd import Start, Group
from aiogram_dialog.widgets.text import Const
from states.categories import GetCategoriesStates
from states.counterparties import GetCounterpartiesStates


menu_admin_start = Group(
    Start(
        text=Const("Категории"),
        id="manage_categories",
        state=GetCategoriesStates.render_main,
    ),
    Start(
        text=Const("Контрагенты"),
        id="manage_counterparties",
        state=GetCounterpartiesStates.render
    ),
    width=2
)
