from aiogram_dialog import Dialog
from operations.not_authorized.authorization.windows import start, authorization


authorization = Dialog(start, authorization, on_close=show_last_window)
