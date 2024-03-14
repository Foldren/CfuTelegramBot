from components.tools import Tool
from modules.gateway.subclasses.counterparty import ApiCounterparty


async def get_counterparties(**kwargs):
    dialog_manager = kwargs['dialog_manager']

    if 'show_distrib' in dialog_manager.dialog_data:
        if dialog_manager.dialog_data['show_distrib']:
            cps_show_mode = 'not_distributed'
        else:
            cps_show_mode = 'distributed'
    else:
        cps_show_mode = 'distributed'

    counterparties = await ApiCounterparty(dm=dialog_manager).get(show_mode=cps_show_mode)
    dict_counterparties = await Tool.get_dict_counterparties(counterparties)

    # Сохраняем контрагентов
    kwargs['dialog_manager'].dialog_data['d_counterparties'] = dict_counterparties

    for c in dict_counterparties:
        c['status'] = '📥 ' if cps_show_mode == 'not_distributed' else ''

    return {
        "counterparties": dict_counterparties,
        "there_are_counterparties": True if counterparties else False,
        "distribution_toggle": [
            {'name': 'Показать не распределенных: 🔴 выкл', 'show_distrib': 'False'},
            {'name': 'Показать не распределенных: 🟢 вкл', 'show_distrib': 'True'},
        ]
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
