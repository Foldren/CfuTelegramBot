import logging
from asyncio import run
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from aredis_om import Migrator
from redis.asyncio import from_url
from components.dialogs import authorization, change_menu, get_categories, get_counterparties, create_category
from config import TOKEN, REDIS_OM_URL
from components import handlers


admin_dialogs = [
    authorization, change_menu, get_categories, create_category, get_counterparties
]


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    redis_conn = await from_url(url=REDIS_OM_URL, db=1, decode_responses=True)
    storage = RedisStorage(redis=redis_conn, key_builder=DefaultKeyBuilder(with_destiny=True))  # В 1 db стейты
    dp = Dispatcher(storage=storage)

    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    dp.include_routers(handlers.rt, *admin_dialogs)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message", "callback_query", "my_chat_member"])


if __name__ == "__main__":
    run(main())
    run(Migrator().run())
