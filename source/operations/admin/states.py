from aiogram.fsm.state import State, StatesGroup


class MenuStates(StatesGroup):
    main = State()


class GetCategoriesLevelStates(StatesGroup):
    render = State()


class AddCategoryStates(StatesGroup):
    select = State()


class EditCategoryStates(StatesGroup):
    select = State()


class DeleteCategoriesStates(StatesGroup):
    select = State()
