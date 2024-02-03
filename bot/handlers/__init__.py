from aiogram import Dispatcher

from . import admin
from . import user


async def setup(dp: Dispatcher):
    await user.setup(dp)
    await admin.setup(dp)
