async def get_text_start_admin(name_user: str) -> str:
    return f"ВКЛЮЧЕН РЕЖИМ АДМИНА 👨‍💼\n\n" \
           f"Здравствуйте, админ <b>{name_user}</b>!👋\n\n" \
           f"‼️ Чтобы настроить бота, вам нужно выполнить 3 шага ‼️\n\n" \
           f"1️⃣️ Завести сотрудников\n" \
           f"2️⃣ Создать ЮР Лица\n" \
           f"3️⃣ Создать категории\n\n" \
           f"<u>Рабочие кнопки бота Управляйки</u> ⚙️ :\n\n" \
           f"1️⃣️ <b>Меню</b> - управление отображением кнопок на разных уровнях " \
           f"вложенности вашего меню. (шаги 2,3)\n" \
           f"2️⃣ <b>Сотрудники</b> - добавление и изменение списка сотрудников, подключенных к боту. (шаг 1)"
