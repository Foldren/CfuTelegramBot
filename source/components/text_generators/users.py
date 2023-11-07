from models import User


async def get_text_dashboard_message(dashboard_data: dict):
    return f"<b>Dashboard</b>\n\n" \
           f"<u>🔸 Продажа товара:</u> <b>{dashboard_data['Продажа товара']}</b>\n" \
           f"<u>🔸 Расходы за период:</u> <b>{dashboard_data['Расходы за период']}</b>\n" \
           f"<u>🔸 Остатки на расчетном счете ИП:</u> <b>{dashboard_data['Остатки на расчетном счете ИП']}</b>\n" \
           f"<u>🔸 К оплате:</u> <b>{dashboard_data['К оплате']}</b>\n" \
           f"<u>🔸 Закупка товара:</u> <b>{dashboard_data['Закупка товара']}</b>\n" \
           f"<u>🔸 Остатки у физ лиц:</u> <b>{dashboard_data['Остатки у физ лиц']}</b>\n" \
           f"<u>🔸 Общая Прибыль:</u> <b>{dashboard_data['Общая Прибыль']}</b>\n" \
           f"<u>🔸 Удержания на МП:</u> <b>{dashboard_data['Удержания на МП']}</b>\n"


async def get_text_fst_start_user(name_user: str) -> str:
    return f"👋 <b>Здравствуйте еще раз, юзер {name_user}</b>!\n\n" \
           f"<u>Рабочие кнопки бота Управляйки</u> ⚙️\n" \
           f"🔹 <b>Операция с категориями</b> - создайте и добавьте новую запись в отчет (лист БД), " \
           f"выбирая нужные категории для позиции в отчете. <i>(категория, это статья движения - " \
           f"доход или расход денежных средств)</i>\n" \
           f"🔹 <b>Операция с подотчетами</b> - выдача в подотчет, возврат подотчета, " \
           f"остаток в подотчете, запрос денег в подотчет.\n" \
           f"🔹 <b>Кошельки</b> - перевод с одного кошелька на другой по выбранному " \
           f"ЮР Лицу и изменение " \
           f"списка ваших кошельков\n" \
           f"🔹 <b>Отчеты</b> - вывод отчетов в зависимости от настройки админа.\n" \
           f"🔹 <b>Поддержка</b> - обращайтесь к нам за помощью, в случае неисправностей, недопонимания" \
           f" или с пожеланиями по доработкам.\n" \
           f"🔹 📩 - уведомления с запросами от сотрудников к вам на подтверждение, " \
           f"ориентируйтесь с помощью групп уведомлений."


async def get_text_start_user(name_user: str) -> str:
    return f"👋 <b>Добро пожаловать, юзер {name_user}</b>!\n\n" \
           f"Теперь вы зарегистрированы в системе ✅\n\n" \
           f"<u>Рабочие кнопки бота Управляйки</u> ⚙️\n" \
           f"🔹 <b>Операция с категориями</b> - создайте и добавьте новую запись в отчет (лист БД), " \
           f"выбирая нужные категории для позиции в отчете. <i>(категория, это статья движения - " \
           f"доход или расход денежных средств)</i>\n" \
           f"🔹 <b>Операция с подотчетами</b> - выдача в подотчет, возврат подотчета, " \
           f"остаток в подотчете, запрос денег в подотчет.\n" \
           f"🔹 <b>Кошельки</b> - перевод с одного кошелька на другой по выбранному " \
           f"ЮР Лицу и изменение " \
           f"списка ваших кошельков\n" \
           f"🔹 <b>Отчеты</b> - вывод отчетов в зависимости от настройки админа.\n" \
           f"🔹 <b>Поддержка</b> - обращайтесь к нам за помощью, в случае неисправностей, недопонимания" \
           f" или с пожеланиями по доработкам.\n" \
           f"🔹 📩 - уведомления с запросами от сотрудников к вам на подтверждение, " \
           f"ориентируйтесь с помощью групп уведомлений."


async def get_msg_notify_new_issuance_of_report(profession_worker: str, fullname_worker: str, ip: str,
                                                nickname_second_worker: str,
                                                volume: str, payment_method: str):
    return f"🆙 {profession_worker.title()} - <b>{fullname_worker}</b>, только что,\nвыдал под отчет новую запись для " \
           f"подтверждения, сотруднику - {nickname_second_worker}\n" \
           f"<u>ЮР Лицо</u>: <b>{ip}</b>\n" \
           f"<u>Сумма</u>: <b>{volume}</b>\n" \
           f"<u>Кошелек</u>: <b>{payment_method}</b>\n"


async def get_msg_notify_new_return_issuance(profession_worker: str, fullname_worker: str, ip: str,
                                             volume: str, payment_method: str):
    return f"↩️ {profession_worker.title()} - <b>{fullname_worker}</b>, только что,\nоформил возврат " \
           f"подотчетных средств\n" \
           f"<u>ЮР Лицо</u>: <b>{ip}</b>\n" \
           f"<u>Сумма</u>: <b>{volume}</b>\n" \
           f"<u>Кошелек</u>: <b>{payment_method}</b>\n"


async def get_msg_notify_new_transfer(profession_worker: str, fullname_worker: str, organization: str,
                                      volume: str, wallet_sender: str, wallet_recipient: str):
    return f"⏩ {profession_worker.title()} - <b>{fullname_worker}</b>, только что,\nоформил перевод:\n" \
           f"<u>ЮР Лицо</u>: <b>{organization}</b>\n" \
           f"<u>Сумма</u>: <b>{volume}</b>\n" \
           f"<u>Кошелек для вывода</u>: <b>{wallet_sender}</b>\n" \
           f"<u>Кошелек для пополнения</u>: <b>{wallet_recipient}</b>\n"


async def get_notify_start_request_report(users_nicknames: list[str], sender_nickname: str, volume: str,
                                          comment: str) -> str:
    return f"<b>🔴  Запрос денежных средств в подотчет</b>\n\n" \
           f"Пользователь {sender_nickname} запросил деньги в подотчет, " \
           f"начата процедура согласования\n" \
           f"<u>Сумма:</u> <b>{volume}</b>\n" \
           f"<u>Комментарий:</u> <b>{comment}</b>\n\n" \
           f"<i>✔ Отмечаю пользователей, которым необходимо согласовать процедуру:\n" \
           f"{' '.join(users_nicknames)}</i>"


async def get_notify_request_report_text(stage: str, sender_nickname: str, volume: int,
                                         comment: str, users_nicknames: list[str] = None) -> str:
    text_v_dict = {
        'conciliate': {
            'status_emoji': '🔴',
            'msg_descr_text': f"Начата процедура согласования.",
            'mark_text': "Отмечаю пользователей, которым необходимо согласовать процедуру:",
        },
        'approve': {
            'status_emoji': '🟡',
            'msg_descr_text': f"Согласование завершено, начат процесс утверждения.",
            'mark_text': "Отмечаю пользователя, которому необходимо подтвердить операцию:",
        },
        'treasure': {
            'status_emoji': '🔵',
            'msg_descr_text': f"Утверждения завершено, начат процесс подтверждения выдачи средств.",
            'mark_text': "Отмечаю пользователя, которому необходимо оформить перевод средств:",
        },
        'end': {
            'status_emoji': '🟢',
            'msg_descr_text': f"Деньги по запросу выданы успешно ✅"
        },
    }

    msg = f"<b>{text_v_dict[stage]['status_emoji']}  Запрос денежных средств в подотчет</b>\n\n" \
          f"{text_v_dict[stage]['msg_descr_text']}\n" \
          f"<u>Запрос от:</u> <b>{sender_nickname}</b>\n" \
          f"<u>Сумма:</u> <b>{str(volume)}</b>\n" \
          f"<u>Комментарий:</u> <b>{comment}</b>\n\n"

    if stage != 'end':
        msg += f"<i>✔ {text_v_dict[stage]['mark_text']}\n" \
               f"{' '.join(users_nicknames)}</i>"

    return msg
