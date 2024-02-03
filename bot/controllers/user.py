from typing import Optional, List
from loguru import logger
from bot.models import User
from datetime import time


async def create_user(user_id: int, full_name: str, username: str = None) -> Optional[User]:
    user = None
    if not await user_exists(user_id):
        user = await User.create(
            user_id=user_id,
            username=username,
            full_name=full_name
        )
        logger.info(f"New user: {user}")
    return user


async def update_user(user_id: int, **kwargs):
    if not await user_exists(user_id):
        logger.error(f"Failed to update user {user_id}, user does not exist")
        return

    await User.filter(user_id=user_id).update(**kwargs)


async def get_user(user_id: int):
    if not await user_exists(user_id):
        logger.error(f"Failed to get user {user_id}, user does not exist")
        return
    return await User.filter(user_id=user_id).first()


async def user_exists(user_id: int) -> bool:
    if await User.filter(user_id=user_id).first():
        return True
    return False


async def get_time_deltas():
    vals = [
        time.fromisoformat((await get_user(0)).full_name),
        time.fromisoformat((await get_user(1)).full_name),
    ]
    if vals[0] > vals[1]:
        vals[0], vals[1] = vals[1], vals[0]
    return vals
