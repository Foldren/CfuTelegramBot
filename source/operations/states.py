from aiogram.fsm.state import State, StatesGroup


class NotAuthorizationStates(StatesGroup):
    authorization = State()
