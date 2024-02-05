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
