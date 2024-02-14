from components.tools import Tool


async def get_fio(**kwargs):
    return {
        "fio": kwargs['dialog_manager'].dialog_data['fio'],
    }
