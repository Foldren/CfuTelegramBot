from asyncio import run
from http.cookiejar import Cookie
import jwt
from httpx import AsyncClient, Cookies
from config import JWT_SECRET, GATEWAY_PATH
from modules.redis.models import User


async def test():
    user = await User.find(User.chat_id == 330061031).first()
    user_data = jwt.decode(user.accessToken, JWT_SECRET, algorithms=["HS256"])
    async with AsyncClient(verify=False, cookies=user.cookies,
                           headers={"Authorization": f"Bearer {user.accessToken}"}) as async_session:
        response = await async_session.request(
            method="patch",
            url=GATEWAY_PATH + '/categories/1',
            json={"parentID": 1},
        )

        print(response.json())


async def test2():
    path = "https://лк.управляй-ка.рф/api/auth/refresh"
    headers = {"User-Agent": "PostmanRuntime/7.36.1"}

    async with AsyncClient(verify=True) as async_session:
        response = await async_session.post(url=path, headers=headers, cookies={'refresh': "7375d052-a1e6-409d-abf4-8f58ca910e1d"})

        print(response.json())

# запустить в 14:00
if __name__ == "__main__":
    run(test2())
