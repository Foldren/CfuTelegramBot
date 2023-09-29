from pathlib import Path
from os import getcwd, getenv
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env

env = Env()
env.read_env('.env')

IS_THIS_LOCAL = "Pycharm" in str(Path.cwd())
REDIS_URL = getenv("REDIS_URL") if IS_THIS_LOCAL else env('REDIS_URL')
TOKEN = getenv("LOCAL_TOKEN_BOT") if IS_THIS_LOCAL else env('TOKEN_BOT')
MYSQL_URL = getenv('MYSQL_URL') if IS_THIS_LOCAL else env("MYSQL_URL")  # getenv для терминала Pycharm
# К сожалению для миграций придется указывать ссылку напрямую
AERICH_CONFIG = {
    "connections": {"default": getenv('MYSQL_URL')},
    "apps": {
        "models": {
            "models": ["source.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}  # "connections": {"default": "sqlite://source/upravlyaika.db"},
MEMORY_STORAGE = MemoryStorage()
BANKS_UPRAVLYAIKA = ["Точка", "Модуль", "Сбер", "Тинькофф", "Альфа", "Наличные", "Другой"]
BANKS_RUS_NAMES = {
    'tinkoff': 'Тинькофф',
    'module': 'Модуль',
    'tochka': 'Точка',
}
STATS_UPRAVLYAIKA = ["Ежедневный", "Еженедельный", "Ежемесячный"]
NAME_GOOGLE_TABLE_BD_LIST = "БД (не редактировать)"
NAME_GOOGLE_TABLE_ACCOUNTING_LIST = "Учёт"
CHECKS_PATH = getcwd() + "/misc/images/checks/"
MAIN_MENU_MSGS = ["Меню", "Сотрудники", "Режим: Админ 👨‍💼", "Операция с категориями", "Операция с подотчетами",
                  "Перевод на кошелек", "Выдача под отчет", "Возврат подотчетных средств", "Режим: Юзер 🙎‍♂️",
                  "Отчеты", "Кошельки", "Изменить кошельки", "⬅️ Назад в главное меню", "Ежедневный", "Еженедельный",
                  "Ежемесячный", "Остаток в подотчете", "/start", "/restart", "Контрагенты", "Банки и расчётные счета"
                  ]  # Все новые reply кнопки добавлять сюда
