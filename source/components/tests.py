from asyncio import run
from modules.redis.models import User


async def main() -> None:
    await User(pk=1).get(pk=1)


if __name__ == '__main__':
    run(main())
