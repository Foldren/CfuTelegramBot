from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const, Format, Multi
from components.text import Text
from events.authorization.authorization import on_authorization
from getters.authorization import get_fio
from states.authorization import AuthorizationStates


start = Window(
    Multi(
        Const('<b>Авторизация</b>'),
        Const("Вы не авторизованы, введите данные для авторизации: логин, пароль.\n" + Text.params_from_new_str),
        Const(Text.example('user', 'password')),
        sep="\n\n"
    ),
    MessageInput(content_types=[ContentType.TEXT], func=on_authorization),
    state=AuthorizationStates.start,
    markup_factory=ReplyKeyboardFactory(input_field_placeholder=Const("Авторизация"))
)

authorization = Window(
    Multi(
        Const(Text.title('Авторизация')),
        Format("👋 Приветствуем {fio}! Авторизация в боте завершена успешно.")
    ),
    state=AuthorizationStates.authorization,
    getter=get_fio
)
