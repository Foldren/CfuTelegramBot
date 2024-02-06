from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from components.callbacks_responses import GetCategoriesCallback
from components.tools import Tool
from modules.gateway.api import ApiGateway
from modules.gateway.responses.category import GetCategoriesResponse
from states.categories import GetCategoriesStates


async def get_child_categories(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, str_item: str):
    item: GetCategoriesCallback = await Tool.callback_to_dataclass(callback, GetCategoriesCallback)
    dialog_manager.dialog_data.setdefault("queue", []).append({"id": item.id, "name": item.name})
    dialog_manager.dialog_data["queue_frmt"] = ' → '.join([c["name"] for c in dialog_manager.dialog_data["queue"]])

    api_gw = ApiGateway(event=callback)
    categories_r: GetCategoriesResponse = await api_gw.get_categories(chat_id=callback.from_user.id, parent_id=item.id)
    categories = categories_r.categories

    dialog_manager.dialog_data["there_are_categories"] = True if categories else False
    dialog_manager.dialog_data["categories"] = [(c.name, c.id) for c in categories]

    await dialog_manager.switch_to(GetCategoriesStates.render_child)


async def get_parent_categories(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    queue = dialog_manager.dialog_data["queue"]
    queue.pop()

    main_menu = False if queue else True

    if main_menu:
        dialog_manager.dialog_data.clear()
        await dialog_manager.switch_to(GetCategoriesStates.render_main)
    else:
        dialog_manager.dialog_data["queue"] = queue
        item_id = int(queue.pop()["id"])

        api_gw = ApiGateway(event=callback)
        categories_r: GetCategoriesResponse = await api_gw.get_categories(chat_id=callback.from_user.id,
                                                                          parent_id=item_id)
        categories = categories_r.categories

        dialog_manager.dialog_data["there_are_categories"] = True if categories else False
        dialog_manager.dialog_data["categories"] = [(c.name, c.id) for c in categories]

        await dialog_manager.switch_to(GetCategoriesStates.render_child)


