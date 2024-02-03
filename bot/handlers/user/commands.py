from loguru import logger

from aiogram import types
from aiogram.filters import CommandObject
from aiogram_dialog import DialogManager, StartMode, ShowMode

from bot.dialogs.user.states import UserMenuStates
from bot.dialogs.admin.states import AdminMenuStates

from bot.controllers import user, test, task


async def cmd_start(message: types.Message, command: CommandObject, dialog_manager: DialogManager):
    await user.create_user(
        message.from_user.id,
        message.from_user.full_name,
        message.from_user.username
    )

    await dialog_manager.start(UserMenuStates.main, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


