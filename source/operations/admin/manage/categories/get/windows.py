from aiogram import F
from aiogram.utils.markdown import bold, underline, italic
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import ScrollingGroup, Cancel, Row, Button, Start
from aiogram_dialog.widgets.text import Const, Multi
from operations.admin.states import GetCategoriesLevelStates, EditCategoryStates, DeleteCategoriesStates, \
    AddCategoryStates

get_categories = Window(
    Multi(
        Const("<b>Категории</b>"),
        Const("📋 Здесь вы можете настроить категории доходов и расходов на разных уровнях "
              "вложенности, для последующего внесения их в вашу гугл таблицу."),
        Const(f"<u>Кнопки управления:</u>\n"
              f"⬅️ - вернуться на уровень выше\n"
              f"➕ - добавить категорию на уровень\n"
              f"✏️ - редактировать категории\n"
              f"❌️ - удалить категории"),
        Const("<i>👉 Для перехода на уровень ниже, нажмите на нужную категорию.</i>"),
        # Const(f"<u>Статус категории:</u>"
        #       f"<i>(если скрыть категорию, ее видимость в боте пропадет для всех "
        #              "пользователей, включая дочерние)</i>"
        #       f"💤 - скрыта"),
        sep="\n\n"
    ),
    Row(
        Start(id="add_category", text=Const("➕"), state=AddCategoryStates.select),
        Start(id="delete_categories", text=Const("❌"), state=DeleteCategoriesStates.select),
        Start(id="edit_category", text=Const("✏️"), state=EditCategoryStates.select),
        Cancel(text=Const("⛔️"))
    ),
    # ScrollingGroup(
    #     F["dialog_data"]["categories"],
    #     id="categories",
    #     width=2,
    #     height=3,
    # ),
    state=GetCategoriesLevelStates.render,
)
