from modules.gateway.api import ApiGateway
from modules.gateway.responses.category import GetCategoriesResponse


async def gtr_get_main_categories(**kwargs):
    callback = kwargs['dialog_manager'].event
    api_gw = ApiGateway(event=callback)
    categories_r: GetCategoriesResponse = await api_gw.get_categories(chat_id=callback.from_user.id, parent_id=None)
    categories = categories_r.categories
    there_are_categories = True if categories else False

    return {
        "categories": [(c.id, c.name) for c in categories_r.categories],
        "there_are_categories": there_are_categories,
    }


async def gtr_get_child_categories(**kwargs):
    return {
        "categories": kwargs['dialog_manager'].dialog_data["categories"],
        "there_are_categories": kwargs['dialog_manager'].dialog_data["there_are_categories"],
    }
