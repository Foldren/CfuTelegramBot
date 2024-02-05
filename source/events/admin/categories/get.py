from typing import Any

import jwt
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from config import JWT_SECRET
from modules.gateway.api import ApiGateway
from modules.gateway.responses.category import GetCategoriesResponse
from modules.redis.models import User
from states.categories import GetCategoriesStates


async def get_child_categories(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    # select_parent_id = callback.data if callback.data != "manage_categories" else None
    dialog_manager.dialog_data.setdefault("queue", []).append(int(item_id))
    api_gw = ApiGateway(event=callback)
    categories_r: GetCategoriesResponse = await api_gw.get_categories(chat_id=callback.from_user.id,
                                                                      parent_id=int(item_id))
    categories = categories_r.categories

    dialog_manager.dialog_data["there_are_categories"] = True if categories else False
    dialog_manager.dialog_data["categories"] = [(c.name, c.id) for c in categories]

    await dialog_manager.switch_to(GetCategoriesStates.render_child)


async def get_parent_categories(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    pass

