from bot.models import User, Test, Task
from bot.controllers import user, test, task

from aiogram_dialog import DialogManager


async def tests_list_getter(**kwargs) -> dict:
    tests = await test.get_all_tests()

    return {"tests": tests}


async def tasks_list_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    tasks = await task.get_user_tasks(dialog_manager.dialog_data["user_id"])
    result = {
        "tasks": tasks,
        "names": dict()
    }

    for _task in tasks:
        _test = await test.find_test(_task.test_id)
        as_str = f"{_test.test_name} "

        if _task.approved == 0:
            as_str += "ждет подтверждения... ⏳"
        elif _task.approved == 1:
            as_str += "отклонен ❎"
        else:
            if _task.mark <= 0:
                as_str += "ждет исполнения... ⏳"
            else:
                as_str += f"выполнен, оценка — {_task.mark} ✅"
        result["names"][_task.task_id] = as_str

    return result


def test_id_getter(_test: Test) -> str:
    return str(_test.test_id)


def task_id_getter(_task: Task) -> str:
    return str(_task.task_id)


async def test_info_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    test_id = dialog_manager.start_data["selected_id"]
    _test = await test.find_test(test_id)

    return {
        "test_id": _test.test_id,
        "test_name": _test.test_name,
        "test_cost": _test.test_cost
    }


async def task_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    task_id = dialog_manager.start_data["task_id"]
    _task = await task.get_task(task_id)
    _test = await test.find_test(_task.test_id)

    return {
        "name": _test.test_name,
        "deadline": _task.deadline,
        "login": _task.login,
        "password": _task.password,
        "status": ["Ожидает подтверждения", "Отклонен", "Подтвержден"][_task.approved],
        "mark": ("Не выставлена" if _task.mark <= 0 else _task.mark),
    }


async def current_order_data_getter(dialog_manager: DialogManager, **kwargs) -> dict:
    _test = await test.find_test(dialog_manager.start_data["selected_id"])
    full_name_exists: bool = dialog_manager.dialog_data.get("full_name", None) is not None
    deadline_date_exists: bool = dialog_manager.dialog_data.get("deadline_date", None) is not None
    deadline_time_exists: bool = dialog_manager.dialog_data.get("deadline_time", None) is not None

    login_exists: bool = dialog_manager.dialog_data.get("login", None) is not None
    password_exists: bool = dialog_manager.dialog_data.get("password", None) is not None

    return {
        "all_filled": full_name_exists and deadline_date_exists and deadline_time_exists,
        "all_login_data_filled": login_exists and password_exists,
        "test_name": _test.test_name,
        "test_cost": _test.test_cost,
        "full_name": dialog_manager.dialog_data.get("full_name", "N/A"),
        "deadline_date": dialog_manager.dialog_data.get("deadline_date", "N/A"),
        "deadline_time": dialog_manager.dialog_data.get("deadline_time", "N/A"),
        "login": dialog_manager.dialog_data.get("login", "N/A"),
        "password": dialog_manager.dialog_data.get("password", "N/A"),
        "full_name_btn_text": ("Изменить ФИО" if full_name_exists else "Ввести ФИО"),
        "deadline_date_btn_text": ("Изменить дату дедлайна" if deadline_date_exists else "Выбрать дату дедлайна"),
        "deadline_time_btn_text": ("Изменить время дедлайна" if deadline_time_exists else "Ввести время дедлайна"),
        "write_login_btn_text": ("Изменить логин" if login_exists else "Ввести логин"),
        "write_password_btn_text": ("Изменить пароль" if password_exists else "Ввести пароль"),
    }
