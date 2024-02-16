from aiogram.fsm.state import StatesGroup, State


class GetCounterpartiesStates(StatesGroup):
    render = State()


class CreateCounterpartyStates(StatesGroup):
    write_params = State()
    select_category = State()


class UpdateCounterpartyStates(StatesGroup):
    select_counterparty = State()
    select_param = State()
    update_inn = State()
    update_name = State()
    attach_new_category = State()


class DeleteCounterpartiesStates(StatesGroup):
    select_counterparties = State()
