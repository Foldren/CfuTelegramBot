from aiogram.fsm.state import StatesGroup, State


class GetCounterpartiesStates(StatesGroup):
    render = State()


class CreateCounterpartyStates(StatesGroup):
    write_params = State()


class DeleteCounterpartiesStates(StatesGroup):
    select = State()
