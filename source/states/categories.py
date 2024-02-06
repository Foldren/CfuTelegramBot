from aiogram.fsm.state import StatesGroup, State


class GetCategoriesStates(StatesGroup):
    render_main = State()
    render_child = State()


class CreateCategoryStates(StatesGroup):
    select_name = State()


class UpdateCategoryStates(StatesGroup):
    select = State()


class DeleteCategoriesStates(StatesGroup):
    select = State()
