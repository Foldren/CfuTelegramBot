from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram_dialog import DialogManager


class Dialog:
    fsm: FSMContext
    d_manager: DialogManager

    def __init__(self, fsm: FSMContext = None, d_manager: DialogManager = None):
        self.fsm = fsm
        self.d_manager = d_manager

    async def set_state(self, state: State):
        await self.fsm.set_state(state)
        await self.d_manager.next()

    async def end(self):
        await self.d_manager.show()
        await self.d_manager.done()
        await self.fsm.clear()
