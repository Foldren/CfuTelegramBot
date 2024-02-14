from typing import Any
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select
from components.callbacks_responses import GetCategoriesCallback
from components.messages_responses import CreateCounterpartyMessage
from components.tools import Tool
from modules.gateway.responses.category import GetCategoriesResponse
from modules.gateway.subclasses.category import ApiCategory


async def on_write_params(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    counterparty: CreateCounterpartyMessage = await Tool.message_to_dataclass(message=message,
                                                                              dataclass_obj=CreateCounterpartyMessage)

    # Формируем начальный список категорий (главных) доступных для прикрепления
    categories_r: GetCategoriesResponse = await ApiCategory(event=message).get(parent_id=None)

    await dialog_manager.update(data={
        "is_child_categories": False,
        'counterparty': {'inn': counterparty.inn, "name": counterparty.name},  # Сохраняем данные контрагента
        'categories': await Tool.get_categories_frmt(categories_r.categories, "has_children")
    }, show_mode=ShowMode.EDIT)

    await dialog_manager.next()


async def on_get_child_categories(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, str_item: str):
    category: GetCategoriesCallback = await Tool.callback_to_dataclass(callback, GetCategoriesCallback)

    # Создаем очередь категорий, записываем в нее id категорий
    dialog_manager.dialog_data.setdefault("queue_categories_id", []).append(category.id)

    categories_r: GetCategoriesResponse = await ApiCategory(event=callback).get(parent_id=category.id)

    await dialog_manager.update(data={
        "is_child_categories": True,
        'categories': await Tool.get_categories_frmt(categories_r.categories, "has_children")
    })
    await dialog_manager.show()


async def on_get_parent_categories(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    queue = dialog_manager.dialog_data["queue_categories_id"]

    # Исключаем из очереди элемент
    queue.pop()

    main_menu = False if queue else True

    if main_menu:
        # Если главное меню чистим данные и меняем флаг дочерних категорий
        dialog_manager.dialog_data.clear()
        dialog_manager.dialog_data["is_child_categories"] = False
    else:
        dialog_manager.dialog_data["is_child_categories"] = True

    # Если очередь осталась значит берем последний элемент из нее как parent_id
    if hasattr(dialog_manager.dialog_data, 'queue_categories_id'):
        parent_category_id = dialog_manager.dialog_data['queue_categories_id'][-1]
    else:
        parent_category_id = None

    categories_r: GetCategoriesResponse = await ApiCategory(event=callback).get(parent_id=parent_category_id)

    await dialog_manager.update(data={
        'categories': await Tool.get_categories_frmt(categories_r.categories, "has_children")
    })
    await dialog_manager.show()
