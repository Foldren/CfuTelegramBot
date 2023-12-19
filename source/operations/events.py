from aiogram_dialog import DialogManager, Data


async def show_last_window(start_data: Data, dialog_manager: DialogManager):
    await dialog_manager.next()
    await dialog_manager.show()
