from typing import Optional
from loguru import logger
from bot.models import Solver


async def create_solver(user_id: int) -> Optional[Solver]:
    user = None
    if not await solver_exists(user_id):
        user = await Solver.create(
            user_id=user_id,
        )
        logger.info(f"New solver: {user}")
    return user


async def get_solvers():
    return await Solver.all()


async def remove_solver(user_id: int):
    await Solver.filter(user_id=user_id).delete()
    logger.info(f"Removed solver: {user_id}")


async def solver_exists(user_id: int) -> bool:
    if await Solver.filter(user_id=user_id).first():
        return True
    return False
