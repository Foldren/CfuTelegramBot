from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Select, Button
from components.dataclasses import DialogCategory
from components.decorators import get_wselect_item
from components.tools import Tool
from modules.gateway.subclasses.category import ApiCategory
from states.categories import GetCategoriesStates


@get_wselect_item(data_cls=DialogCategory, items_name='d_categories')
async def on_get_children(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                          selected_category: DialogCategory):
    # Создаем очередь категорий чтобы по ней перемещаться
    dialog_manager.dialog_data.setdefault("queue", []).append({
        "id": selected_category.id,
        "name": selected_category.name
    })

    # Максимальный уровень вложенности 5, ставим проверку
    if len(dialog_manager.dialog_data['queue']) == 5:
        await callback.answer("⛔️ Максимальный уровень вложенности категории 5.", show_alert=True)
        dialog_manager.dialog_data['queue'].pop()
        return

    categories = await ApiCategory(event=callback).get(parent_id=selected_category.id)
    dict_categories = await Tool.get_dict_categories(categories, "status")

    dialog_manager.dialog_data.update({
        'd_categories': dict_categories,
        "there_are_categories": True if categories else False,
        "queue_frmt": ' → '.join([c["name"] for c in dialog_manager.dialog_data["queue"]])
    })

    # Если окно главное переключаем на окно дочернее
    if dialog_manager.current_context().state == GetCategoriesStates.render_main:
        await dialog_manager.switch_to(GetCategoriesStates.render_child)
    else:
        await dialog_manager.show()


async def on_get_parents(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    queue = dialog_manager.dialog_data["queue"]

    # Удаляем последний элемент очереди
    queue.pop()

    # Форматируем очередь
    dialog_manager.dialog_data["queue_frmt"] = ' → '.join([c["name"] for c in queue])
    main_menu = False if queue else True

    if main_menu:
        dialog_manager.dialog_data.clear()
        await dialog_manager.switch_to(GetCategoriesStates.render_main)
    else:
        # Если не главное меню берем id последнего элемента очереди как parent_id
        categories = await ApiCategory(event=callback).get(parent_id=queue[-1]['id'])

        dialog_manager.dialog_data.update({
            "queue": queue,
            "d_categories": await Tool.get_dict_categories(categories, "status"),
            "there_are_categories": True if categories else False
        })

        await dialog_manager.show(show_mode=ShowMode.EDIT)
