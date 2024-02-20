from aiogram.filters import BaseFilter
from aiogram.types import Message
from modules.redis.models import User
from modules.redis.redis_om import RedisOM


class IsNotAuthorizedFilter(BaseFilter):
    async def __call__(self, message: Message, redis: RedisOM) -> bool:
        try:
            await redis.get(User, pk=message.from_user.id)
            return False
        except:
            return True


class IsAuthorizedFilter(BaseFilter):

    async def __call__(self, message: Message, redis: RedisOM) -> bool:
        try:
            await redis.get(User, pk=message.from_user.id)
            return True
        except:
            return False


