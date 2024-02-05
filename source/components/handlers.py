from aiogram import Router, F
from aiogram.types import Message, BotCommandScopeAllPrivateChats
from aiogram_dialog import DialogManager, StartMode
from components.commands import commands
from components.filters import IsNotAuthorizedFilter, IsAuthorizedFilter
from states.authorization import AuthorizationStates
from states.menu import MenuStates

rt = Router()
rt.message.filter(F.chat.type == "private")


@rt.message(F.text.in_({"/start"}), IsNotAuthorizedFilter())
async def authorization(message: Message, dialog_manager: DialogManager):
    await message.bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
    await dialog_manager.start(state=AuthorizationStates.start, mode=StartMode.RESET_STACK)


@rt.message(F.text.in_({"/start"}), IsAuthorizedFilter())
async def restart(message: Message, dialog_manager: DialogManager):
    await message.bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
    await dialog_manager.start(state=MenuStates.main, mode=StartMode.RESET_STACK)
