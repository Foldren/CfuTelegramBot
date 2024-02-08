from aiogram.fsm.state import StatesGroup, State


class GetCategoriesStates(StatesGroup):
    render_main = State()
    render_child = State()


class CreateCategoryStates(StatesGroup):
    select_name = State()


class UpdateCategoryStates(StatesGroup):
    select_category = State()
    select_param = State()
    update_name = State()


class DeleteCategoriesStates(StatesGroup):
    select_categories = State()
