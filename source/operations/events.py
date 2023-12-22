from aiogram_dialog import DialogManager, Data, ShowMode
from operations.not_authorized.states import AuthorizationStates


async def open_last_window(start_data: Data, dialog_manager: DialogManager):
    await dialog_manager.next()
    await dialog_manager.show()
