from modules.gateway.api import ApiGateway
from modules.gateway.responses.category import GetCategoriesResponse
from modules.gateway.responses.counterparty import GetCounterpartiesResponse
from modules.gateway.subclasses.category import ApiCategory
from modules.gateway.subclasses.counterparty import ApiCounterparty


# categories -----------------------------------------------------------------------------------------------------------

async def gtr_get_main_categories(**kwargs):
    callback = kwargs['dialog_manager'].event
    api_gw = ApiCategory(event=callback)
    categories_r: GetCategoriesResponse = await api_gw.get(parent_id=None)
    categories = categories_r.categories
    kwargs['dialog_manager'].dialog_data['parent_id'] = None

    return {
        "categories": [(c.id, c.name, "" if c.status == 1 else "💤") for c in categories_r.categories],
        "there_are_categories": True if categories else False
    }


async def gtr_get_categories_for_update_and_delete(**kwargs):
    callback = kwargs['dialog_manager'].event
    parent_id = kwargs['dialog_manager'].start_data['parent_id']
    api_gw = ApiCategory(event=callback)
    categories_r: GetCategoriesResponse = await api_gw.get(parent_id=parent_id)

    return {
        "categories": [(c.id, c.name, "" if c.status == 1 else "💤", int(c.status)) for c in categories_r.categories]
    }


# counterparties -------------------------------------------------------------------------------------------------------

async def gtr_get_counterparties(**kwargs):
    callback = kwargs['dialog_manager'].event
    api_gw = ApiCounterparty(event=callback)
    counterparties_r: GetCounterpartiesResponse = await api_gw.get()

    return {
        "counterparties": [(c.name, c.inn) for c in counterparties_r.counterparties],
    }
