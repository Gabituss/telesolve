from bot.models import User, Test, Task
from bot.controllers import user, test, task

from aiogram_dialog import DialogManager

from loguru import logger


async def tests_list_getter(**kwargs) -> dict:
    tests = await test.get_all_tests()

    return {"tests": tests}


async def current_test_data_getter(dialog_manager: DialogManager, **kwargs):
    name_exists: bool = dialog_manager.dialog_data.get("name", None) is not None
    cost_exists: bool = dialog_manager.dialog_data.get("cost", None) is not None

    return {
        "all_filled": name_exists and cost_exists,
        "name": dialog_manager.dialog_data.get("name", "N/A"),
        "cost": dialog_manager.dialog_data.get("cost", "N/A"),
        "name_btn": ("Изменить название" if name_exists else "Ввести название"),
        "cost_btn": ("Изменить цену" if cost_exists else "Ввести цену")
    }


async def test_data_getter(dialog_manager: DialogManager, **kwargs):
    test_id = dialog_manager.start_data["test_id"]
    _test = await test.find_test(test_id)

    return {
        "name": _test.test_name,
        "cost": _test.test_cost,
    }


async def task_data_getter(dialog_manager: DialogManager, **kwargs):
    task_id = dialog_manager.start_data["task_id"]
    _task = await task.get_task(task_id)
    _user = await user.get_user(_task.user_id)
    _test = await test.find_test(_task.test_id)
    mark_radio = dialog_manager.find("r_marks")

    return {
        "test_name": _test.test_name,
        "full_name": _task.full_name,
        "username": _user.username,
        "deadline": _task.deadline,
        "login": _task.login,
        "password": _task.password,
        "not_started": _task.mark == -1,
        "started": _task.mark == 0,
        "finished": _task.mark > 0,
        "marks": [(i, i) for i in range(1, 6)],
        "show_send": mark_radio.get_checked() is not None and _task.mark == 0,
        "status": ["Ожидает подтверждения", "Отклонен", "Подтвержден"][_task.approved],
        "mark": ("Не выставлена" if _task.mark <= 0 else _task.mark),
    }
