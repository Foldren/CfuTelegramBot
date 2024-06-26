from typing import Any
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select
from components.dataclasses import CreateCounterpartyMessage, DialogCategory
from components.decorators import get_wselect_item
from components.tools import Tool
from modules.gateway.subclasses.category import ApiCategory
from modules.gateway.subclasses.counterparty import ApiCounterparty
from states.counterparties import CreateCounterpartyStates


async def on_start_create_counterparty(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    categories = await ApiCategory(dm=dialog_manager).get()

    if categories:
        await dialog_manager.start(state=CreateCounterpartyStates.write_params)
    else:
        await callback.answer(text="⛔️ Сначала создайте хотя бы одну категорию.", show_alert=True)


async def on_write_params(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    counterparty: CreateCounterpartyMessage = await Tool.message_to_dataclass(message=message,
                                                                              dataclass_obj=CreateCounterpartyMessage)

    # Формируем начальный список категорий (главных) доступных для прикрепления
    categories = await ApiCategory(dm=dialog_manager).get(parent_id=None, include_static=True)

    dialog_manager.dialog_data.update({
        "is_child_categories": False,
        'counterparty': {'inn': counterparty.inn, "name": counterparty.name},  # Сохраняем данные контрагента
        'd_categories': await Tool.get_dict_categories(categories, "has_children")
    })

    await dialog_manager.next()


@get_wselect_item(data_cls=DialogCategory, items_name='d_categories')
async def on_get_child_categories(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                                  selected_category: DialogCategory):
    # Создаем очередь категорий, записываем в нее id категорий
    dialog_manager.dialog_data.setdefault("queue_categories_id", []).append(selected_category.id)

    categories = await ApiCategory(dm=dialog_manager).get(parent_id=selected_category.id, include_static=True)

    if selected_category.hasChildren == 1:
        dialog_manager.dialog_data.update({
            "is_child_categories": True,
            'd_categories': await Tool.get_dict_categories(categories, "has_children")
        })
        await dialog_manager.show(show_mode=ShowMode.EDIT)
    else:
        await ApiCounterparty(dm=dialog_manager).create(inn=dialog_manager.dialog_data['counterparty']['inn'],
                                                        name=dialog_manager.dialog_data['counterparty']['name'],
                                                        category_id=selected_category.id)

        s_c_name = selected_category.name.replace("🔹 ", "")
        await callback.answer(text=f"✅ Контрагент добавлен успешно.\n"
                                   f"Категория - '{s_c_name}', прикреплена на распределение.",
                              show_alert=True)
        await dialog_manager.done()


async def on_get_parent_categories(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    queue = dialog_manager.dialog_data["queue_categories_id"]

    # Исключаем из очереди элемент
    queue.pop()

    main_menu = False if queue else True

    if main_menu:
        # Если главное меню чистим данные и меняем флаг дочерних категорий
        dialog_manager.dialog_data.pop("d_categories")
        dialog_manager.dialog_data.pop("queue_categories_id")
        dialog_manager.dialog_data["is_child_categories"] = False
    else:
        dialog_manager.dialog_data["is_child_categories"] = True

    # Если очередь осталась значит берем последний элемент из нее как parent_id
    if hasattr(dialog_manager.dialog_data, 'queue_categories_id'):
        parent_category_id = dialog_manager.dialog_data['queue_categories_id'][-1]
    else:
        parent_category_id = None

    categories = await ApiCategory(dm=dialog_manager).get(parent_id=parent_category_id, include_static=True)
    dialog_manager.dialog_data['d_categories'] = await Tool.get_dict_categories(categories, "has_children")
    await dialog_manager.show(show_mode=ShowMode.EDIT)
