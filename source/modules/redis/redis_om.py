from dataclasses import dataclass
from redis.asyncio import Redis, from_url


class RedisOM:
    __db: Redis

    def __init__(self, db: int, url: str) -> None:
        self.__db = from_url(url=url, db=db, decode_responses=True)

    async def get(self, model_cls_type: dataclass, pk: str | int):
        key_name = model_cls_type.__name__ + ":" + str(pk)
        response = await self.__db.get(key_name)
        return model_cls_type.from_json(response)

    async def save(self, model_cls: dataclass):
        key_name = type(model_cls).__name__ + ":" + str(model_cls.pk)
        await self.__db.set(key_name, str(model_cls.to_json()))

    async def delete(self, model_cls_type: dataclass, pk: str | int):
        key_name = model_cls_type.__name__ + ":" + str(pk)
        await self.__db.delete(key_name)
