from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from components.callbacks_responses import GetCategoriesCallback
from components.tools import Tool
from modules.gateway.responses.category import GetCategoriesResponse
from modules.gateway.subclasses.category import ApiCategory
from states.categories import GetCategoriesStates


async def on_get_children(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, str_item: str):
    category: GetCategoriesCallback = await Tool.callback_to_dataclass(callback, GetCategoriesCallback)
    dialog_manager.dialog_data.setdefault("queue", []).append({"id": category.id, "name": category.name})
    dialog_manager.dialog_data["queue_frmt"] = ' → '.join([c["name"] for c in dialog_manager.dialog_data["queue"]])

    api_gw = ApiCategory(event=callback)
    categories_r: GetCategoriesResponse = await api_gw.get(parent_id=category.id)
    categories = categories_r.categories

    dialog_manager.dialog_data['parent_id'] = category.id
    dialog_manager.dialog_data["there_are_categories"] = True if categories else False
    dialog_manager.dialog_data["categories"] = [(c.name, c.id, "" if c.status == 1 else "💤") for c in categories]

    await dialog_manager.switch_to(GetCategoriesStates.render_child)


async def on_get_parents(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    queue = dialog_manager.dialog_data["queue"]
    queue.pop()

    main_menu = False if queue else True

    if main_menu:
        dialog_manager.dialog_data.clear()
        await dialog_manager.switch_to(GetCategoriesStates.render_main)
    else:
        dialog_manager.dialog_data["queue"] = queue
        category_id = int(queue.pop()["id"])

        api_gw = ApiCategory(event=callback)
        categories_r: GetCategoriesResponse = await api_gw.get(parent_id=category_id)
        categories = categories_r.categories

        dialog_manager.dialog_data['parent_id'] = category_id
        dialog_manager.dialog_data["there_are_categories"] = True if categories else False
        dialog_manager.dialog_data["categories"] = [(c.name, c.id, "" if c.status == 1 else "💤") for c in categories]

        await dialog_manager.switch_to(GetCategoriesStates.render_child)
