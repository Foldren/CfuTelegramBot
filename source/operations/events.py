from aiogram_dialog import DialogManager, Data, ShowMode


async def del_and_open_next_window(start_data: Data, dialog_manager: DialogManager):
    await dialog_manager.next()
    await dialog_manager.show(show_mode=ShowMode.DELETE_AND_SEND)
