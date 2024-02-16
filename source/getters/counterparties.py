from components.tools import Tool
from modules.gateway.subclasses.counterparty import ApiCounterparty


async def get_counterparties(**kwargs):
    callback = kwargs['dialog_manager'].event
    counterparties = await ApiCounterparty(event=callback).get()
    dict_counterparties = await Tool.get_dict_counterparties(counterparties)

    # Сохраняем контрагентов
    kwargs['dialog_manager'].dialog_data['d_counterparties'] = dict_counterparties

    return {
        "counterparties": dict_counterparties,
    }


async def get_selected_counterparty(**kwargs):
    return {
        "selected_counterparty": kwargs['dialog_manager'].dialog_data['selected_counterparty'],
    }


async def get_attach_categories(**kwargs):
    return {
        "categories": kwargs['dialog_manager'].dialog_data['d_categories'],
        "is_child_categories": kwargs['dialog_manager'].dialog_data['is_child_categories']
    }
