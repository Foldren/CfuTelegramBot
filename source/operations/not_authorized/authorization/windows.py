from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Next
from aiogram_dialog.widgets.text import Const, Format, Multi
from components.text import Text
from operations.not_authorized.authorization.events import on_authorization
from operations.not_authorized.states import AuthorizationStates


start = Window(
    Multi(
        Const(Text.title('Авторизация')),
        Const("Вы не авторизованы, введите данные для авторизации: логин, пароль."),
        Const(Text.params_from_new_str),
        Const(Text.example('user', 'password'))
    ),
    MessageInput(content_types=[ContentType.TEXT], func=on_authorization),
    state=AuthorizationStates.start
)

authorization = Window(
    Multi(
        Const(Text.title('Авторизация')),
        Format("👋 Приветствуем {dialog_data[fio]}! Авторизация в боте завершена успешно.")
    ),
    state=AuthorizationStates.authorization
)
