from aiogram.fsm.state import State, StatesGroup


class AuthorizationStates(StatesGroup):
    start = State()
    authorization = State()
