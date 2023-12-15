from asyncio import run
from components.text import Text

title = run(Text.title('Авторизация'))
example_start = run(Text.example('user', 'password'))


async def send_data():
    return f"{title}" \
           f"Вы не авторизованы, введите данные для авторизации: " \
           f"логин, пароль." \
           f"{Text.params_from_new_str}" \
           f"{example_start}"


async def authorization(fio: str):
    return f"{title}" \
           f"👋 Приветствуем {fio}! Авторизация в боте завершена успешно."
