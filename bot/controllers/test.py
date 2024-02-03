from typing import Optional
from loguru import logger
from bot.models import Test

from tortoise.expressions import Q


async def create_test(test_id: int, test_name: str, test_cost: int, visible: bool) -> Optional[Test]:
    test = None
    if not await test_exists(test_id):
        test = await Test.create(
            test_id=test_id,
            test_name=test_name,
            test_cost=test_cost,
            visible=visible
        )
        logger.info(f"New test {test_id} {test_name} {test_cost}")
    return test


async def remove_test(test_id: int):
    if not await test_exists(test_id):
        logger.error(f"Failed to remove test {test_id}, test does not exit")
        return
    await Test.filter(test_id=test_id).delete()
    logger.info(f"Removed test {test_id}")


async def update_test(test_id: int, **kwargs):
    if not await test_exists(test_id):
        logger.error(f"Failed to update test {test_id}, test does not exist")
        return

    await Test.filter(test_id=test_id).update(**kwargs)


async def find_test(test_id: int) -> Optional[Test]:
    if not await test_exists(test_id):
        return None
    return await Test.filter(test_id=test_id).first()


async def get_all_tests(visible=True) -> list[Test]:
    return await Test.filter((Q(visible=visible) | Q(visible=True))).all()


async def get_all_tests_names() -> list[str]:
    _tests = await Test.all()
    res = [_test.test_name for _test in _tests]

    return res


async def remove_all_tests():
    logger.info(f"DELETE ALL TESTS 😈")
    await Test.all().delete()


async def test_exists(test_id: int) -> bool:
    if await Test.filter(test_id=test_id).first():
        return True
    return False


async def get_new_id() -> int:
    return await Test.all().count()
