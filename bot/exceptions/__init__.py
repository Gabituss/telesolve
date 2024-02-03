from aiogram import Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from bot.exceptions.errors import on_unknown_state, on_unknown_intent


def setup(dp: Dispatcher):
    dp.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    dp.errors.register(on_unknown_state, ExceptionTypeFilter(UnknownState))
