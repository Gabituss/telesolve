import logging
from aiogram_dialog import DialogManager, StartMode, ShowMode

from bot.dialogs.user.states import UserMenuStates

from aiogram.types.error_event import ErrorEvent


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(UserMenuStates.main, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def on_unknown_state(event: ErrorEvent, dialog_manager: DialogManager):
    logging.error("Restarting dialog %s", event.exception)
    await dialog_manager.start(UserMenuStates.main, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)
