from aiogram.fsm.state import StatesGroup, State


class AuthorizationStates(StatesGroup):
    start = State()
    authorization = State()
