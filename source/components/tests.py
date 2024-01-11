from asyncio import run
from httpx import AsyncClient

from config import GATEWAY_PATH


async def test():
    async with AsyncClient() as async_session:
        response = await async_session.request(
            method="post",
            url=GATEWAY_PATH + "/auth/sign-in",
            headers={'Content-Type': 'application/json'},
            json={"email": "test", "password": "442424"}
        )
        print(response.json())


if __name__ == "__main__":
    run(test())
