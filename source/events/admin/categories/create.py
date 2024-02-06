from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput


async def on_select_name(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    print(dialog_manager.current_context().dialog_data)

    # api_gw = ApiGateway(event=message)
    # await api_gw.create_category(chat_id=message.chat.id, parent_id=item_id)
    await message.answer("Категория успешно добавлена в систему ✅", show_alert=True)
    await dialog_manager.done()


