from pathlib import Path
from os import getenv
from dotenv import load_dotenv

load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(Path.cwd())
GATEWAY_PATH = getenv("GATEWAY_PATH")
REDIS_URL = getenv("REDIS_URL")
TOKEN = getenv("LOCAL_TOKEN_BOT") if IS_THIS_LOCAL else getenv("TOKEN_BOT")
SECRET_KEY = getenv("SECRET_KEY")
TECHNICAL_SUPPORT_GROUP_CHAT_ID = -4023565993
BANKS_UPRAVLYAIKA = ["Точка", "Модуль", "Сбер", "Тинькофф", "Альфа", "Наличные", "Другой"]
BANKS_RUS_NAMES = {
    'tinkoff': 'Тинькофф',
    'module': 'Модуль',
    'tochka': 'Точка',
}
SUPER_ADMINS_CHAT_ID = [330061031, 708742962]
STATS_UPRAVLYAIKA = ["Ежедневный", "Еженедельный", "Ежемесячный", "Dashboard", "Чеки"]
MAIN_MENU_MSGS = ["Меню", "Сотрудники", "Режим: Админ 👨‍💼", "Операция с категориями", "Операция с подотчетами",
                  "Перевод на кошелек", "Выдача в подотчет", "Возврат подотчета", "Режим: Юзер 🙎‍♂️",
                  "Отчеты", "Управление отчетами", "Кошельки", "Изменение списка кошельков", "⬅️ Назад в главное меню",
                  "Ежедневный", "Еженедельный", "Категории", "ЮР Лица",
                  "Ежемесячный", "Остаток в подотчете", "/start", "/restart", "Контрагенты", "Банки и расчётные счета",
                  "Поддержка", "Назначение ролей", "Табель"
                  ]  # Все новые reply кнопки добавлять сюда
STAGES_REPS_REQS_BY_ROLE = {
    'conciliator': 'conciliate',
    'approver': 'approve',
    'treasurer': 'treasure',
}
ROLE_BY_STAGES_REPS_REQS = {
    'conciliate': 'conciliator',
    'approve': 'approver',
    'treasure': 'treasurer',
}
ROLES = ['timekeeper']
DEFINE_STATUSES = ["🔴 Не пришел:", "🟢 На работе:", "🔵 Ушел:"]
