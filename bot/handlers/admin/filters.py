from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.controllers import solver


class SolverFilter(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        return await solver.solver_exists(message.from_user.id)
