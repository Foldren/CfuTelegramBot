from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from components.filters import IsAdminFilter
from components.keyboards import cf_key_start_admin

rt = Router()

# Фильтр на проверку категории доступа пользователя
rt.message.filter(IsAdminFilter())
rt.callback_query.filter(IsAdminFilter())


# Хэндлер на команду /start
@rt.message(Command(commands=["start"]))
async def start_admin(message: Message, state: FSMContext):
    await state.clear()

    message_text = f"Здравствуйте, админ <b>{message.from_user.full_name}</b>!👋\n\n" \
                   f"‼️ Чтобы настроить бота, вам нужно выполнить 3 шага ‼️\n\n"\
                   f"1️⃣️ Завести сотрудников\n"\
                   f"2️⃣ Создать ЮР Лица\n"\
                   f"3️⃣ Создать категории\n\n"\
                   f"<u>Рабочие кнопки бота Управляйки</u> ⚙️ :\n\n" \
                   f"1️⃣️ <b>Меню</b> - управление отображением кнопок на разных уровнях " \
                   f"вложенности вашего меню. (шаги 2,3)\n" \
                   f"2️⃣ <b>Сотрудники</b> - добавление и изменение списка сотрудников, подключенных к боту. (шаг 1)"

    await message.answer(message_text, reply_markup=cf_key_start_admin, parse_mode='html')
