from aiogram.types import BotCommand


commands = [
    BotCommand(command="start", description="запустить (перезапустить) бота"),
    BotCommand(command="signin", description="авторизоваться"),
    BotCommand(command="logout", description="выйти из профиля"),
]
