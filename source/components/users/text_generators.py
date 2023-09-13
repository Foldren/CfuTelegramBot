async def get_text_fst_start_user(name_user: str) -> str:
    return f"Здравствуйте еще раз, юзер <b>{name_user}</b>!👋\n\n" \
           f"<u>Рабочие кнопки бота Управляйки</u> ⚙️ :\n\n" \
           f"1️⃣️ <b>Новая запись</b> - создайте и добавьте новую запись в отчет (лист БД), выбирая нужные " \
           f"категории для позиции в отчете.\n" \
           f"2️⃣ <b>Выдача под отчет</b> - создание 2 записей в бд с уведомлением в группу для " \
           f"подтверждения сотрудником"


async def get_text_start_user(name_user: str) -> str:
    return f"Добро пожаловать, юзер <b>{name_user}</b>!👋\n\n" \
           f"Теперь вы зарегистрированы в системе ✅\n\n" \
           f"<u>Рабочие кнопки бота Управляйки</u> ⚙️ :\n\n" \
           f"1️⃣️ <b>Новая запись</b> - создайте и добавьте новую запись в отчет (лист БД), выбирая нужные " \
           f"категории для позиции в отчете." \
           f"2️⃣ <b>Выдача под отчет</b> - создание 2 записей в бд с уведомлением в группу для " \
           f"подтверждения сотрудником"


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
