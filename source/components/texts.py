# ADMINS ---------------------------------------------------------------------------------------------------------------
# > Manage menu items --------------------------------------------------------------------------------------------------

text_get_list_categories = f"Здесь вы можете настроить кнопки и очередь ответов вашего бота Управляйки.\n\n" \
                           f"<code>Кнопки управления</code>:\n\n" \
                           f"⬅️ - вернуться на уровень выше\n" \
                           f"➕ - добавить категорию на уровень\n" \
                           f"✏️ - редактировать категории\n" \
                           f"❌️ - удалить категории\n\n" \
                           f"Для перехода на уровень меню ниже, нажмите на нужную категорию 👉\n\n" \
                           f"<code>Статус категории</code>:\n" \
                           f"(если скрыть категорию, ее видимость в боте пропадет для всех " \
                           f"пользователей, включая дочерние)\n\n" \
                           f"💤 - скрыта\n\n"

text_start_add_menu_item = f"\nВведите название новой категории 🆕👇:"

text_choose_observers_menu_item = f"\nТеперь выберите сотрудников, которые смогут видеть этот пункт меню"

text_end_add_menu_item = f"Пункт меню успешно добавлен в систему ✅"

text_choose_param_to_change_menu_item = "\nВыберите параметр, который хотите изменить в пункте меню 👉📊"

text_start_change_menu_item = "\nНажмите на пункт меню, который нужно изменить 👉"

text_change_name_menu_item = f"\nВведите новое название категории 🆕👇:"

text_end_change_name_menu_item = f"Название пункта меню изменено успешно ✅"

text_start_change_observers_menu_item = f"\nВыберите пользователей, которым будет виден выбранный пункт меню 👉👨‍💼"

text_end_change_observers_menu_item = f"Наблюдатели пункта меню изменены успешно ✅"

text_start_delete_menu_item = "\nВыберите пункты меню, которые нужно удалить 👉"

text_stop_delete_menu_item = "Операция удаления отменена ❎"

text_end_delete_menu_item = "Пункты меню удалены успешно ✅"

text_stop_delete_u = "Операция по анулированию доступов отменена ❎"

text_end_delete_u = "Пользователи успешно удалены из бота ✅"

# > Manage_users -------------------------------------------------------------------------------------------------------

text_get_list_users = f"Здесь вы можете настроить доступы ваших сотрудников к боту Управляйке.\n\n" \
                      f"<code>Кнопки управления</code>:\n\n" \
                      f"➕ - добавить пользователя\n" \
                      f"✏️ - редактировать\n" \
                      f"❌️ - забрать доступ"

text_start_add_user = f"Введите данные пользователя:\n\n" \
                      f"1️⃣ Имя пользователя - в телеграм указан со значком @\n" \
                      f"2️⃣ ФИО - введите через пробел (фамилия имя отчество)\n" \
                      f"3️⃣ Должность сотрудника\n\n" \
                      f"Каждый параметр, начиная со второго вводите с новой строки в формате, " \
                      f"указанном ниже 📋👨‍💼\n\n" \
                      f"Пример:\n<code>@user987\nПочетов Сергей Александрович\nменеджер</code>"

text_get_id_user = "🔵 Перешлите сюда сообщение этого пользователя,\nчтобы я мог взять его chat_id 📨🆔\n" \
                   "(у пользователя в настройках конфиденциальности должна быть разрешена 'пересылка сообщений')\n\n" \
                   "🔵 Либо просто укажите chat_id в формате числа👇"

text_invalid_user_id = "Указан невалидный chat_id ⚠️"

text_end_add_user = f"Теперь пользователь подключен к боту ✅"

text_user_exists = f"Упс, похоже пользователь с этим chat_id уже зарегистрирован в боте 🤷‍♂️"

text_start_change_user = "Нажмите на сотрудника, данные которого нужно изменить 👇"

text_change_user = f"Введите новые данные пользователя:\n\n" \
                   f"1️⃣ Имя пользователя - в телеграм указан со значком @\n" \
                   f"2️⃣ ФИО - введите через пробел (фамилия имя отчество)\n" \
                   f"3️⃣ Должность сотрудника\n\n" \
                   f"Каждый параметр, начиная со второго вводите с новой строки в формате, " \
                   f"указанном ниже 📋👨‍💼 " \
                   f"(также вы просто можете скопировать пример, в нем указаны данные выбранного пользователя)\n\n" \
                   f"Пример:\n"

text_end_change_user = f"Данные пользователя изменены ✅"

text_end_change_id_user = f"id пользователя изменен ✅🆔"

text_get_id_change_user = "🔵 Перешлите сюда сообщение пользователя,\nчтобы я мог взять его chat_id 📨🆔\n" \
                          "(у пользователя в настройках конфиденциальности должна быть разрешена 'пересылка сообщений')\n\n" \
                          "🔵 Либо просто укажите новый chat_id в формате числа👇"

text_start_delete_users = "\nВыберите пользователей, у которых нужно забрать доступ 👉"


# USERS ----------------------------------------------------------------------------------------------------------------
# > manage menu items --------------------------------------------------------------------------------------------------

text_get_user_list_mi = f"Задайте нужную очередь категорий для внесения новой записи в бд.\n\n" \
                        f"<code>Кнопки управления</code>:\n\n" \
                        f"Назад ⬅️ - вернуться на уровень выше\n" \
                        f"Расход ➖ - новая запись о расходе\n" \
                        f"Доход ➕ - новая запись о доходе\n\n" \
                        f"Для перехода на уровень меню ниже, нажмите на нужную категорию 👉\n\n"

text_no_menu_items_u = f"Вы добавлены в бот, но похоже админ еще не назначил доступные для вас категории 🙅‍♀️"

text_start_add_mi_to_bd = f"<b>ШАГ</b> 1️⃣:\nВведите сумму операции в рублях, в формате числа 💵\n<b>Пример</b>:" \
                          f"\n<code>987654</code>"

text_choose_bank = f"<b>ШАГ</b> 2️⃣:\nВыберите банк, по которому произведена операция 🏦 (либо способ оплаты наличными): \n"

text_invalid_volume_operation = "Некорректная сумма. Введите число 💯"

text_send_check_photo = "<b>ШАГ</b> 3️⃣:\nПеретащите в чат фото чека 🖼️\n(в сжатом виде или в виде файла)" \
                        "\n\n Либо нажмите - 📎 чтобы прикрепить файл."

text_invalid_check_photo = "Похоже вы отправили не фото 🤷‍♂️"

text_end_add_mi_to_bd = f"Запись успешно добавлена в лист БД ✅\n" \
                        f"Чек можно получить с помощью кнопки - Получить чеки 📄" \
                        f"\n\n🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩"

# > join bot to group --------------------------------------------------------------------------------------------------

text_success_join_bot_to_group = f"Похоже меня добавили в группу. Здравствуйте, коллеги," \
                                 f" я - <b>Бот Управляйка</b> 🙎‍♂️👋\n\n" \
                                 f"Вижу приглашение отправлено от одного из пользователей, зарегистрированный " \
                                 f"в моей системе. \nОкей, уведомления о новых операциях вашей организации буду " \
                                 f"присылать в этот чат 💬"

text_repeat_add = f"Я уже прикреплен к другой группе, чтобы "