from typing import Optional
from loguru import logger
from bot.models import Task

from tortoise.expressions import Q


async def create_task(**kwargs) -> Task:
    task = None
    if not await task_exists(kwargs.get("task_id")):
        task = await Task.create(**kwargs)

    return task


async def task_exists(task_id: int) -> bool:
    if await Task.filter(task_id=task_id).first():
        return True
    return False


async def get_task(task_id: int) -> Task:
    return await Task.filter(task_id=task_id).first()


async def remove_task(task_id: int):
    return await Task.filter(task_id=task_id).delete()


async def get_all_tasks(show_hidden: bool = True) -> list[Task]:
    return await Task.filter((Q(hidden=show_hidden) | Q(hidden=False)))


async def get_user_tasks(user_id: int, show_hidden: bool = True) -> list[Task]:
    return await Task.filter((Q(hidden=show_hidden) | Q(hidden=False)) & (Q(user_id=user_id))).all()


async def update_task(task_id: int, **kwargs):
    if not await task_exists(task_id):
        logger.error(f"Failed to update task {task_id}, task does not exist")
        return

    await Task.filter(task_id=task_id).update(**kwargs)


async def get_new_id() -> int:
    return await Task.all().count()
