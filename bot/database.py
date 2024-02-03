from tortoise import Tortoise, run_async
from config import DB_FILE


async def init():
    await Tortoise.init(
        db_url=f'sqlite://{DB_FILE}',
        modules={'models': ['bot.models']}
    )
    await Tortoise.generate_schemas()


run_async(init())
