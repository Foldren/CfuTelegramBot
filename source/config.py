from pathlib import Path
from os import environ
from dotenv import load_dotenv


IS_THIS_LOCAL = "Pycharm" in str(Path.cwd())

if not IS_THIS_LOCAL:
    load_dotenv()

GATEWAY_PATH = environ["GATEWAY_PATH"]
JWT_SECRET = environ["JWT_SECRET"]
REDIS_OM_URL = environ["REDIS_OM_URL"]
TOKEN = environ["TOKEN_BOT"]
UA_TELEGRAM = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) " \
              "Version/15.3 Mobile/15E148 Safari/604.1 Telegram 3.6.112)"
