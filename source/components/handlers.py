from aiogram import Router, F
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.types import Message, BotCommandScopeAllPrivateChats
from aiogram_dialog import DialogManager, StartMode
from components.commands import commands
from components.filters import IsNotAuthorizedFilter, IsAuthorizedFilter
from modules.gateway.subclasses.category import ApiCategory
from modules.redis.models import User
from modules.redis.redis_om import RedisOM
from states.authorization import AuthorizationStates
from states.menu import MenuStates

rt = Router()
rt.message.filter(F.chat.type == "private")


@rt.message(F.text == "/start", IsAuthorizedFilter())
async def restart(message: Message, dialog_manager: DialogManager):
    try:
        await ApiCategory(dm=dialog_manager).get()
        await dialog_manager.start(state=MenuStates.main, mode=StartMode.RESET_STACK)
    except CancelHandler:
        pass


@rt.message(F.text.in_({"/start", '/signin', '/logout'}), IsNotAuthorizedFilter())
async def sign_in(message: Message, dialog_manager: DialogManager):
    await message.bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())
    await dialog_manager.start(state=AuthorizationStates.start, mode=StartMode.RESET_STACK)


@rt.message(F.text == "/logout", IsAuthorizedFilter())
async def log_out(message: Message, dialog_manager: DialogManager, redis: RedisOM):
    await message.answer("🏃 Вы вышли из аккаунта.")
    await redis.delete(User, message.from_user.id)
    await dialog_manager.start(state=AuthorizationStates.start, mode=StartMode.RESET_STACK)
