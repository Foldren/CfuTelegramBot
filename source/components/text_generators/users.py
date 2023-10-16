from models import User


async def get_text_fst_start_user(name_user: str) -> str:
    return f"Здравствуйте еще раз, юзер <b>{name_user}</b>!👋\n\n" \
           f"<u>Рабочие кнопки бота Управляйки</u> ⚙️ :\n\n" \
           f"1️⃣️ <b>Операция с категориями</b> - создайте и добавьте новую запись в отчет (лист БД), выбирая нужные " \
           f"категории для позиции в отчете (категория, это статья движения - приход или расход денежных средств).\n\n" \
           f"2️⃣ <b>Операция с подотчетами</b> - получение и возврат подотчета\n\n" \
           f"3️⃣ <b>Кошельки</b> - перевод с одного кошелька на другой по выбранному ЮР Лицу и изменение " \
           f"списка ваших кошельков\n\n" \
           f"4️⃣ <b>Отчеты</b> - вывод отчетов в зависимости от настройки админа."


async def get_text_start_user(name_user: str) -> str:
    return f"Добро пожаловать, юзер <b>{name_user}</b>!👋\n\n" \
           f"Теперь вы зарегистрированы в системе ✅\n\n" \
           f"<u>Рабочие кнопки бота Управляйки</u> ⚙️ :\n\n" \
           f"1️⃣️ <b>Операция с категориями</b> - создайте и добавьте новую запись в отчет (лист БД), выбирая нужные " \
           f"категории для позиции в отчете (категория, это статья движения - приход или расход денежных средств).\n\n" \
           f"2️⃣ <b>Операция с подотчетами</b> - получение и возврат подотчета\n\n" \
           f"3️⃣ <b>Кошельки</b> - перевод с одного кошелька на другой по выбранному ЮР Лицу и изменение " \
           f"списка ваших кошельков\n\n" \
           f"4️⃣ <b>Отчеты</b> - вывод отчетов в зависимости от настройки админа."


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
    return f"<b>🟡  Запрос в подотчет</b>\n\n" \
           f"Пользователь {sender_nickname} запросил деньги в подотчет, " \
           f"начата процедура согласования\n" \
           f"<u>Сумма:</u> <b>{volume}</b>\n" \
           f"<u>Комментарий:</u> <b>{comment}</b>\n\n" \
           f"<i>✔ Отмечаю пользователей, которым необходимо согласовать процедуру</i>\n" \
           f"{' '.join(users_nicknames)}"
