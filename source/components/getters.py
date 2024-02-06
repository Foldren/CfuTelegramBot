from modules.gateway.api import ApiGateway
from modules.gateway.responses.category import GetCategoriesResponse
from modules.gateway.responses.counterparty import GetCounterpartiesResponse


# categories -----------------------------------------------------------------------------------------------------------

async def gtr_get_main_categories(**kwargs):
    callback = kwargs['dialog_manager'].event
    api_gw = ApiGateway(event=callback)
    categories_r: GetCategoriesResponse = await api_gw.get_categories(chat_id=callback.from_user.id, parent_id=None)
    categories = categories_r.categories

    return {
        "categories": [(c.id, c.name) for c in categories_r.categories],
        "there_are_categories": True if categories else False
    }


# counterparties -------------------------------------------------------------------------------------------------------

async def gtr_get_counterparties(**kwargs):
    callback = kwargs['dialog_manager'].event
    api_gw = ApiGateway(event=callback)
    counterparties_r: GetCounterpartiesResponse = await api_gw.get_counterparties(chat_id=callback.from_user.id)

    return {
        "counterparties": [(c.name, c.inn) for c in counterparties_r.counterparties],
    }
