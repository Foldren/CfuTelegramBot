from aiogram_dialog import Dialog, LaunchMode
from operations.not_authorized.authorization.windows import start, authorization


authorization = Dialog(start, authorization, launch_mode=LaunchMode.SINGLE_TOP)
