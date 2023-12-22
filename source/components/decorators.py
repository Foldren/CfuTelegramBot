from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput


def cancel_event_handler(func):
    async def _wrapper(message: Message, widget: MessageInput, dialog_manager: DialogManager):
        try:
            result = await func(message, widget, dialog_manager)
            return result
        except CancelHandler:
            pass
    return _wrapper
