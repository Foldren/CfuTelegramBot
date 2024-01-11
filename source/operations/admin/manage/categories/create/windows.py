from asyncio import run
from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format, Multi
from components.text import Text
from operations.not_authorized.authorization.events import on_authorization
from operations.not_authorized.states import AuthorizationStates

title = run(Text.title('Авторизация'))
example_start = run(Text.example('user', 'password'))


start = Window(
    Multi(
        Const(title),
        Const("Вы не авторизованы, введите данные для авторизации: логин, пароль."),
        Const(Text.params_from_new_str),
        Const(example_start)
    ),
    MessageInput(content_types=[ContentType.TEXT], func=on_authorization),
    state=AuthorizationStates.start
)

authorization = Window(
    Multi(
        Const(title),
        Format("👋 Приветствуем {dialog_data[fio]}! Авторизация в боте завершена успешно.")
    ),
    state=AuthorizationStates.authorization
)
