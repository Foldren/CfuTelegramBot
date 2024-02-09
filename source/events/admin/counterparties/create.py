from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from components.messages_responses import CreateCounterpartyMessage
from components.tools import Tool


async def on_write_params(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    counterparty: CreateCounterpartyMessage = await Tool.message_to_dataclass(message=message,
                                                                              dataclass_obj=CreateCounterpartyMessage)

    dialog_manager.dialog_data['counterparty'] = {'inn': counterparty.inn, "name": counterparty.name}

    await message.answer("Категория успешно добавлена в систему ✅")
    await dialog_manager.done()
