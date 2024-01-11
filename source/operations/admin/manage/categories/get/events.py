from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from components.tools import Tool
from modules.gateway.api import ApiGateway
from modules.gateway.responses.category import GetCategoriesResponse


async def on_get_categories(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    redis = dialog_manager.middleware_data["redis"]
    user_cid = callback.from_user.id
    token = (await redis.user.get(chat_id=user_cid)).accessToken
    select_parent_id = callback.data if callback.data != "manage_categories" else None
    api_gw = ApiGateway(user_chat_id=user_cid, access_token=token)
    categories_r = await api_gw.get_categories(user_id=callback.from_user.id, parent_id=select_parent_id)
    categories = await Tool.handle_exceptions(categories_r, callback.message, GetCategoriesResponse)

    print(categories)




