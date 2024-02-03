import asyncio

from loguru import logger

from bot import botlogging, mics, handlers, dialogs, exceptions, database
from bot.mics import dp, bot

import config
from aiogram_dialog.tools import render_preview


async def main():
    dialogs.setup(dp)
    exceptions.setup(dp)
    await handlers.setup(dp)
    await botlogging.setup()
    await mics.setup()


if __name__ == '__main__':
    asyncio.run(main())
