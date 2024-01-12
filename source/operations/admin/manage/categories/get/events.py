from typing import Union
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from components.tools import Tool
from modules.gateway.api import ApiGateway
from modules.gateway.responses.category import GetCategoriesResponse


async def on_get_categories(event: Union[Message, CallbackQuery], button: Button, dialog_manager: DialogManager):
    redis = dialog_manager.middleware_data["redis"]
    chat_id = dialog_manager.event.from_user.id
    # select_parent_id = callback.data if callback.data != "manage_categories" else None
    api_gw = ApiGateway(redis=redis, event=dialog_manager.event)
    categories_r = await api_gw.get_categories(chat_id=chat_id, parent_id=None)
    print(categories_r)




