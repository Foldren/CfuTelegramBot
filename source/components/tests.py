from asyncio import run
from datetime import datetime, timedelta
from http.cookiejar import Cookie

import jwt
from aiohttp import CookieJar
from httpx import AsyncClient, Cookies
from config import JWT_SECRET, GATEWAY_PATH
from modules.redis.models import User


async def test():
    user = await User.find(User.chat_id == 330061031).first()
    user_data = jwt.decode(user.accessToken, JWT_SECRET, algorithms=["HS256"])
    async with AsyncClient(verify=False, cookies=user.cookies,
                           headers={"Authorization": f"Bearer {user.accessToken}"}) as async_session:
        response = await async_session.request(
            method="get",
            url=GATEWAY_PATH + '/categories',
            params={
                "userID": user_data['id'],
                "parentID": 1
            },
        )

        print(response.json())


async def test2():
    # user = await User.find(User.chat_id == 330061031).first()
    # user_data = jwt.decode(user.accessToken, JWT_SECRET, algorithms=["HS256"], options={"verify_signature": False})
    # print(user_data)
    # print(user.cookies)
    # user.cookies["Path"] = "/"
    # user.cookies["Expires"] = "Sat, 03 Aug 2024 14:42:17 GMT"
    #
    kwargs = {
        "version": 0,
        "name": "refresh",
        "value": "04b3de45-8312-4db4-868b-8ad9129c449f",
        "port": None,
        "port_specified": False,
        "domain": "xn--j1ab.xn----7sbbg9ahe3aj2a1l.xn--p1ai",
        "domain_specified": True,
        "domain_initial_dot": False,
        "path": "/",
        "path_specified": True,
        "secure": True,
        "expires": (datetime.now() + timedelta(days=365)).toordinal(),
        "discard": True,
        "comment": None,
        "comment_url": None,
        "rest": {"HttpOnly": True},
        "rfc2109": False,
    }
    cookie = Cookie(**kwargs)  # type: ignore
    cookies = Cookies()
    cookies.jar.set_cookie(cookie)

    async with AsyncClient() as async_session:
        response = await async_session.post(
            url=GATEWAY_PATH + "/auth/refresh",
            cookies=cookies
        )

        print(response.json())


if __name__ == "__main__":
    run(test2())
