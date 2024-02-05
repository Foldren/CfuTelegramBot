from asyncio import run, create_task, get_event_loop
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const
from modules.gateway.api import ApiGateway
from modules.gateway.responses.category import GetCategoriesResponse
from states.categories import GetCategoriesStates


def get_main_categories_btns_list(callback: CallbackQuery):
    api_gw = ApiGateway(event=callback)
    # categories_r: GetCategoriesResponse = get_event_loop().run_until_complete(api_gw.get_categories(chat_id=callback.from_user.id, parent_id=None))
    # return [SwitchTo(text=Const(c.name),
    #                  id=str(c.id),
    #                  state=GetCategoriesStates.render_child) for c in categories_r.categories]
