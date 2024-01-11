from aiogram_dialog import Window
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const, Format, Multi
from components.reply_keyboards import menu_admin_start
from operations.admin.states import MenuStates


main = Window(
    Multi(
        Const('<b>Режим Админа 👨‍💼</b>'),
        Format("👋 Здравствуйте, админ <b>{event.from_user.username}</b>"),
        Const(f"<u>Рабочие кнопки бота Управляйки в режиме админа ⚙️</u>\n"
              f"<b>🔹 Категории</b> - управление отображением категорий на разных уровнях вложенности. "
              f"<i>(категория - тип расхода или дохода, например 'начисление зп')</i>"),
        sep="\n\n"
    ),
    menu_admin_start,
    state=MenuStates.main,
    markup_factory=ReplyKeyboardFactory(resize_keyboard=True, input_field_placeholder=Format("Главное меню"))
)
