import logging
from asyncio import run
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio import from_url
from config import TOKEN, REDIS_URL
from modules.redis.user import RedisUser
from operations import handlers
from modules.redis.redis import Redis
from operations.not_authorized import handlers as authorization_handlers
from operations.not_authorized.dialogs import authorization

# admin_routers = [
#     start_admin.rt, get_list_categories.rt, add_category.rt, get_list_users.rt, add_user.rt,
#     change_user.rt, change_category.rt, delete_category.rt, delete_user.rt, change_mode.rt,
#     manage_users_stats.rt, get_list_organizations.rt, add_organization.rt, delete_organizations.rt,
#     get_list_partners.rt, add_partner.rt, delete_partners.rt, get_list_banks.rt, add_bank.rt, delete_banks.rt,
#     get_list_payment_accounts.rt, add_payment_account.rt, delete_payment_accounts.rt, manage_users_roles.rt
# ]
#
# user_routers = [
#     start_user.rt, browse_categories.rt, write_chosen_category_to_bd.rt, write_issuance_of_report_to_bd.rt,
#     write_return_of_report_to_bd.rt, choose_write_category_sender.rt, write_transfer_to_wallet_to_bd.rt,
#     open_nested_menu.rt, change_wallets_list.rt, show_user_stats.rt, get_balance_in_report.rt,
#     open_admin_nested_menu.rt, request_money_report.rt
# ]
#
# member_routers = [
#     check_events_notification_groups.rt, confirm_issuance_report.rt, technical_support.rt,
#     manage_confirm_notifications.rt, write_new_report_card_user.rt
# ]
#
# super_admin_routers = [
#     add_new_client.rt
# ]

not_authorize_routers = [
    authorization_handlers.rt
]

dialogs = [
    authorization
]


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)

    storage = RedisStorage(
        redis=await from_url(REDIS_URL, db=0, decode_responses=True),
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )  # В 15 db стейты

    dp = Dispatcher(storage=storage)

    user = RedisUser(user_db=await from_url(REDIS_URL, db=1, decode_responses=True))
    redis = Redis(user)

    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(*not_authorize_routers, handlers.rt, *dialogs)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        redis=redis,
        allowed_updates=["message", "callback_query", "my_chat_member"]
    )


if __name__ == "__main__":
    run(main())
