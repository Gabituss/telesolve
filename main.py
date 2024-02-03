import asyncio
import logging
import datetime
from config import TOKEN

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

logging.basicConfig(
    level=logging.INFO,
    filename=f"logs/{datetime.datetime.now().strftime('%Y:%m:%d-%H log')}"
)

bot = Bot(token=TOKEN)

dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Hello there!")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
