import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from loguru import logger

import config

loop = asyncio.get_event_loop()

storage = MemoryStorage()
bot = Bot(token=config.TELEGRAM_BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot=bot, loop=loop, storage=storage)


async def setup():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
