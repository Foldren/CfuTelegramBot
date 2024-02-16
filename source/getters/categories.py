from components.tools import Tool
from modules.gateway.responses.children import DCategory
from modules.gateway.subclasses.category import ApiCategory


async def get_main_ones(**kwargs):
    callback = kwargs['dialog_manager'].event
    categories: list[DCategory] = await ApiCategory(event=callback).get(parent_id=None)
    dict_categories = await Tool.get_dict_categories(categories, "status")

    kwargs['dialog_manager'].dialog_data['d_categories'] = dict_categories

    return {
        "categories": dict_categories,
        "there_are_categories": True if categories else False
    }


async def get_children(**kwargs):
    return {
        "categories": kwargs['dialog_manager'].dialog_data['d_categories'],
        "there_are_categories": kwargs['dialog_manager'].dialog_data['there_are_categories'],
        "queue_frmt": kwargs['dialog_manager'].dialog_data['queue_frmt']
    }


async def get_for_update_or_delete(**kwargs):
    callback = kwargs['dialog_manager'].event
    parent_id = kwargs['dialog_manager'].start_data['parent_id']
    categories: list[DCategory] = await ApiCategory(event=callback).get(parent_id=parent_id)
    dict_categories = await Tool.get_dict_categories(categories, "status")

    kwargs['dialog_manager'].dialog_data['d_categories'] = dict_categories

    return {
        "categories": dict_categories
    }


async def get_selected_category(**kwargs):
    return {
        'selected_category': kwargs['dialog_manager'].dialog_data['selected_category']
    }
