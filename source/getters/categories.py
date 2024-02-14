from components.tools import Tool
from modules.gateway.responses.category import GetCategoriesResponse
from modules.gateway.subclasses.category import ApiCategory


async def get_main_ones(**kwargs):
    callback = kwargs['dialog_manager'].event
    categories_r: GetCategoriesResponse = await ApiCategory(event=callback).get(parent_id=None)
    categories = categories_r.categories

    return {
        "categories": await Tool.get_categories_frmt(categories, "status"),
        "there_are_categories": True if categories else False
    }


async def get_children(**kwargs):
    return {
        "categories": kwargs['dialog_manager'].dialog_data['categories'],
        "there_are_categories": kwargs['dialog_manager'].dialog_data['there_are_categories'],
        "queue_frmt": kwargs['dialog_manager'].dialog_data['queue_frmt']
    }


async def get_for_update_or_delete(**kwargs):
    callback = kwargs['dialog_manager'].event
    parent_id = kwargs['dialog_manager'].start_data['parent_id']
    categories_r: GetCategoriesResponse = await ApiCategory(event=callback).get(parent_id=parent_id)
    categories = categories_r.categories

    return {
        "categories": await Tool.get_categories_frmt(categories, "status")
    }


async def get_selected_category(**kwargs):
    return {
        'selected_category': kwargs['dialog_manager'].dialog_data['selected_category']
    }
