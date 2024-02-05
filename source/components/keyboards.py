from aiogram_dialog.widgets.kbd import Start, Group
from aiogram_dialog.widgets.text import Const
from states.categories import GetCategoriesStates


menu_admin_start = Group(
    Start(
        text=Const("Категории"),
        id="manage_categories",
        state=GetCategoriesStates.render_main
    )
)
