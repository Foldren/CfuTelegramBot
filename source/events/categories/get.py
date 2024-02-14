from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Select
from components.callbacks_responses import GetCategoriesCallback
from components.tools import Tool
from modules.gateway.responses.category import GetCategoriesResponse
from modules.gateway.subclasses.category import ApiCategory
from states.categories import GetCategoriesStates


async def on_get_children(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, str_item: str):
    category: GetCategoriesCallback = await Tool.callback_to_dataclass(callback, GetCategoriesCallback)

    # Создаем очередь категорий чтобы по ней перемещаться
    dialog_manager.dialog_data.setdefault("queue", []).append({
        "id": category.id,
        "name": category.name
    })

    if len(dialog_manager.dialog_data['queue']) == 5:
        await callback.answer("⛔️ Максимальный уровень вложенности категории 5.", show_alert=True)
        dialog_manager.dialog_data['queue'].pop()
        return

    categories_r: GetCategoriesResponse = await ApiCategory(event=callback).get(parent_id=category.id)
    categories = categories_r.categories

    await dialog_manager.update(data={
        "categories": await Tool.get_categories_frmt(categories, "status"),
        "there_are_categories": True if categories else False,
        "queue_frmt": ' → '.join([c["name"] for c in dialog_manager.dialog_data["queue"]])
    }, show_mode=ShowMode.EDIT)

    # Если окно главное переключаем на окно дочернее
    if dialog_manager.current_context().state == GetCategoriesStates.render_main:
        await dialog_manager.switch_to(GetCategoriesStates.render_child)


async def on_get_parents(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    queue = dialog_manager.dialog_data["queue"]

    # Удаляем последний элемент очереди
    queue.pop()

    # Форматиируем очередь
    dialog_manager.dialog_data["queue_frmt"] = ' → '.join([c["name"] for c in queue])
    main_menu = False if queue else True

    if main_menu:
        dialog_manager.dialog_data.clear()
        await dialog_manager.switch_to(GetCategoriesStates.render_main)
    else:
        # Если не главное меню берем id последнего элемента очереди как parent_id
        categories_r: GetCategoriesResponse = await ApiCategory(event=callback).get(parent_id=queue[-1]['id'])
        categories = categories_r.categories

        await dialog_manager.update(data={
            "queue": queue,
            "categories": await Tool.get_categories_frmt(categories, "status"),
            "there_are_categories": True if categories else False
        }, show_mode=ShowMode.EDIT)
