from dataclasses import dataclass
from typing import Any
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from components.tools import Tool


def get_wselect_item(data_cls: dataclass, items_name: str, item_param: str = "id"):
    """
    Декоратор для установки в аргумент функции выбранного элемента из select,
    находит элемент в items по полю id

    :param data_cls: датакласс будущего объекта item
    :param items_name: название items в dialog_data (объект items должен быть типа list[dict])
    :param item_param: параметр dict по которому искать item
    :return:
    """
    def _upper(func):
        async def _wrapper(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
            selected_item: data_cls = await Tool.get_item_from_dict(
                items=dialog_manager.dialog_data[items_name],
                param=item_param,
                value=int(item_id),
                dataclass_obj=data_cls
            )
            result = await func(callback, widget, dialog_manager, selected_item)

            return result

        return _wrapper

    return _upper
