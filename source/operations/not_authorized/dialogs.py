from aiogram_dialog import Dialog, LaunchMode
from operations.events import open_last_window
from operations.not_authorized.authorization.windows import start, authorization


authorization = Dialog(start, authorization, launch_mode=LaunchMode.ROOT, on_close=open_last_window)
