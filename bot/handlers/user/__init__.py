from aiogram import Dispatcher
from aiogram.filters import Command

from bot.handlers.user.commands import *


async def setup(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
