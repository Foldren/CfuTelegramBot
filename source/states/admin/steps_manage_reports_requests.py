from aiogram.fsm.state import State, StatesGroup


class StepsManageReportsRequests(StatesGroup):
    select_role_reports_requests = State()

