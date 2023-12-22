from aiogram import F
from aiogram.utils.markdown import bold, underline, italic
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import ScrollingGroup
from aiogram_dialog.widgets.text import Const, Multi
from operations.admin.states import GetCategoriesLevelStates

get_categories = Window(
                    Multi(
                        Const(bold("Категории\n")),
                        Const("📋 Здесь вы можете настроить категории доходов и расходов на разных уровнях "
                              "вложенности, для последующего внесения их в вашу гугл таблицу.\n"),
                        Const(underline("Кнопки управления:")),
                        Const(f"⬅️ - вернуться на уровень выше\n"
                              f"➕ - добавить категорию на уровень\n"
                              f"✏️ - редактировать категории\n"
                              f"❌️ - удалить категории\n"),
                        Const(italic("👉 Для перехода на уровень ниже, нажмите на нужную категорию.\n")),
                        Const(underline("Статус категории:")),
                        Const(italic("(если скрыть категорию, ее видимость в боте пропадет для всех "
                                     "пользователей, включая дочерние)")),
                        Const("💤 - скрыта")
                    ),
                    ScrollingGroup(
                        F["dialog_data"]["categories"],
                        id="categories",
                        width=2,
                        height=3,
                    ),
                    state=GetCategoriesLevelStates.render,
                 )
