import logging
from asyncio import run
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from redis.asyncio import from_url
from components.dialogs import authorization, change_menu, get_categories, get_counterparties, create_category, \
    update_category, delete_categories, create_counterparty, delete_counterparties, update_counterparty
from config import TOKEN, REDIS_OM_URL
from components import handlers
from modules.redis.redis_om import RedisOM


admin_dialogs = [
    authorization, change_menu,
    get_categories, create_category, update_category, delete_categories,
    get_counterparties, create_counterparty, update_counterparty, delete_counterparties
]


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    redis_conn = await from_url(url=REDIS_OM_URL, db=1, decode_responses=True)
    storage = RedisStorage(redis=redis_conn, key_builder=DefaultKeyBuilder(with_destiny=True))  # В 1 db стейты
    dp = Dispatcher(storage=storage)

    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(handlers.rt, *admin_dialogs)
    setup_dialogs(dp)

    redis_om = RedisOM(db=0, url=REDIS_OM_URL)  # В 0 db модели redis

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, redis=redis_om, allowed_updates=["message", "callback_query", "my_chat_member"])


if __name__ == "__main__":
    run(main())
