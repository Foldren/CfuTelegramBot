from modules.gateway.responses.counterparty import GetCounterpartiesResponse
from modules.gateway.subclasses.counterparty import ApiCounterparty


async def get_counterparties(**kwargs):
    callback = kwargs['dialog_manager'].event
    counterparties_r: GetCounterpartiesResponse = await ApiCounterparty(event=callback).get()

    return {
        "counterparties": [(c.inn, c.name) for c in counterparties_r.counterparties],
    }


async def get_attach_categories(**kwargs):
    return {
        "categories": kwargs['dialog_manager'].dialog_data['categories'],
        "is_child_categories": kwargs['dialog_manager'].dialog_data['is_child_categories']
    }
