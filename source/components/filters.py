from traceback import print_exc
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aredis_om import Migrator
from modules.redis.models import User


class IsNotAuthorizedFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            await User.find(User.chat_id == message.from_user.id).first()
            return False
        except:
            return True


class IsAuthorizedFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            await User.find(User.chat_id == message.from_user.id).first()
            return True
        except:
            return False
