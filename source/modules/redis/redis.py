from dataclasses import dataclass
from modules.redis.user import RedisUser


@dataclass
class Redis:
    __slots__ = {"user"}
    user: RedisUser

