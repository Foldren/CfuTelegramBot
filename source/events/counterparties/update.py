from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, Button
from components.dataclasses import DialogCounterparty, DialogCategory
from components.decorators import get_wselect_item
from components.tools import Tool
from modules.gateway.subclasses.category import ApiCategory
from modules.gateway.subclasses.counterparty import ApiCounterparty
from states.counterparties import UpdateCounterpartyStates


@get_wselect_item(data_cls=DialogCounterparty, items_name='d_counterparties')
async def on_select_counterparty(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                                 selected_counterparty: DialogCounterparty):
    dialog_manager.dialog_data['selected_counterparty'] = DialogCounterparty.to_dict(selected_counterparty)
    categories = await ApiCategory(dm=dialog_manager).get()
    dialog_manager.dialog_data.update({
        'd_categories': await Tool.get_dict_categories(categories, extended_option="has_children"),
        'is_child_categories': False
    })

    await dialog_manager.next()


async def on_back_to_counterparties(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    counterparties = await ApiCounterparty(dm=dialog_manager).get()

    # Завершаем диалог и обновляем список контрагентов
    await dialog_manager.done()
    dialog_manager.dialog_data["d_counterparties"] = await Tool.get_dict_counterparties(counterparties)
    await dialog_manager.show(show_mode=ShowMode.EDIT)


async def on_update_name(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    selected_counterparty = DialogCounterparty.from_dict(dialog_manager.dialog_data['selected_counterparty'])
    api_c = ApiCounterparty(dm=dialog_manager)

    await api_c.update(counterparty_id=selected_counterparty.id, name=message.text)

    counterparties = await api_c.get()

    await message.answer("Название контрагента изменено успешно ✅")

    dialog_manager.dialog_data['selected_counterparty']['name'] = message.text
    dialog_manager.dialog_data['d_counterparties'] = await Tool.get_dict_counterparties(counterparties)

    await dialog_manager.switch_to(UpdateCounterpartyStates.select_param, show_mode=ShowMode.DELETE_AND_SEND)


async def on_update_inn(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    selected_counterparty: DialogCounterparty = (
        DialogCounterparty.from_dict(dialog_manager.dialog_data['selected_counterparty']))
    api_c = ApiCounterparty(dm=dialog_manager)

    await api_c.update(counterparty_id=selected_counterparty.id, inn=message.text)

    counterparties = await api_c.get()

    await message.answer("ИНН контрагента изменено успешно ✅")

    dialog_manager.dialog_data['selected_counterparty']['inn'] = message.text
    dialog_manager.dialog_data['counterparties'] = await Tool.get_dict_counterparties(counterparties)

    await dialog_manager.switch_to(UpdateCounterpartyStates.select_param, show_mode=ShowMode.DELETE_AND_SEND)


@get_wselect_item(data_cls=DialogCategory, items_name='d_categories')
async def on_get_child_categories(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                                  selected_category: DialogCategory):
    # Создаем очередь категорий, записываем в нее id категорий
    dialog_manager.dialog_data.setdefault("queue_categories_id", []).append(selected_category.id)

    categories = await ApiCategory(dm=dialog_manager).get(parent_id=selected_category.id)

    if selected_category.hasChildren == 1:
        dialog_manager.dialog_data.update({
            "is_child_categories": True,
            'd_categories': await Tool.get_dict_categories(categories, "has_children")
        })
        await dialog_manager.show(show_mode=ShowMode.EDIT)
    else:
        selected_counterparty = DialogCounterparty.from_dict(dialog_manager.dialog_data['selected_counterparty'])
        await ApiCounterparty(dm=dialog_manager).update(counterparty_id=selected_counterparty.id,
                                                     category_id=selected_category.id)

        s_c_name = selected_category.name.replace("🔹 ", "")
        await callback.answer(text=f"✅ К контрагенту прикреплена новая категория на распределение - "
                                   f"'{s_c_name}'",
                              show_alert=True)

        dialog_manager.dialog_data['selected_counterparty']['categoryName'] = s_c_name
        await dialog_manager.switch_to(UpdateCounterpartyStates.select_param, show_mode=ShowMode.DELETE_AND_SEND)


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

    categories = await ApiCategory(dm=dialog_manager).get(parent_id=parent_category_id)
    dialog_manager.dialog_data['d_categories'] = await Tool.get_dict_categories(categories, "has_children")
    await dialog_manager.show(show_mode=ShowMode.EDIT)
