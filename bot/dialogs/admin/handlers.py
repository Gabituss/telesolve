from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import ShowMode

from bot.dialogs.admin import getters
from bot.dialogs.admin.states import AdminMenuStates, TestMenuStates
from bot.dialogs.user.filters import process_time
from bot.controllers import test, task, solver, user

from typing import Any
from loguru import logger
from datetime import date

from bot.worksheet import Updater

upd = Updater("token.json")


async def clear_order_data(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    dialog_manager.dialog_data.clear()


async def write_name(event, widget, dialog_manager: DialogManager, *_):
    name = dialog_manager.find("name_input").get_value()
    dialog_manager.dialog_data.update(name=name)
    await dialog_manager.switch_to(AdminMenuStates.add_new_test)


async def write_cost(event, widget, dialog_manager: DialogManager, *_):
    cost = dialog_manager.find("cost_input").get_value()
    dialog_manager.dialog_data.update(cost=cost)
    await dialog_manager.switch_to(AdminMenuStates.add_new_test)


async def create_test(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    data = await getters.current_test_data_getter(dialog_manager)
    test_id = await test.get_new_id()

    _test = await test.create_test(
        test_id=test_id,
        test_name=data["name"],
        test_cost=int(data["cost"]),
        visible=True
    )

    await callback.answer("Test created", show_alert=True)
    await clear_order_data(callback, None, dialog_manager)
    await dialog_manager.switch_to(AdminMenuStates.tests_management)


async def select_test(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, selected_item: str):
    _test = await test.find_test(int(selected_item))

    await dialog_manager.start(TestMenuStates.main, data={"test_id": _test.test_id})


async def go_back(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await callback.message.delete()
    await dialog_manager.done()


async def delete(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await test.update_test(dialog_manager.start_data["test_id"], visible=False)
    await callback.answer("Удалено", show_alert=True)
    await dialog_manager.done()


async def change_test_name(event, widget, dialog_manager: DialogManager, *_):
    name = dialog_manager.find("name_input").get_value()
    test_id = dialog_manager.start_data["test_id"]

    await test.update_test(test_id, test_name=name)
    await dialog_manager.switch_to(TestMenuStates.main)
    await upd.update_tasks_list()


async def change_test_cost(event, widget, dialog_manager: DialogManager, *_):
    cost = int(dialog_manager.find("cost_input").get_value())
    test_id = dialog_manager.start_data["test_id"]

    await test.update_test(test_id, test_cost=cost)
    await dialog_manager.switch_to(TestMenuStates.main)


async def add_solver(event, widget, dialog_manager: DialogManager, *_):
    user_id = int(dialog_manager.find("solver_add_input").get_value())

    await solver.create_solver(user_id)

    await dialog_manager.switch_to(AdminMenuStates.solvers_management)


async def remove_solver(event, widget, dialog_manager: DialogManager, *_):
    user_id = int(dialog_manager.find("solver_remove_input").get_value())

    await solver.remove_solver(user_id)

    await dialog_manager.switch_to(AdminMenuStates.solvers_management)


async def update_time(event, widget, dialog_manager: DialogManager, *_):
    l, r = dialog_manager.find("time_input").get_value().split("-")
    l = process_time(l)
    r = process_time(r)

    await user.update_user(0, full_name=l)
    await user.update_user(1, full_name=r)

    await dialog_manager.switch_to(AdminMenuStates.main)


async def start_solving_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    task_id = int(dialog_manager.start_data["task_id"])

    await task.update_task(task_id, mark=0)
    await upd.update_tasks_list()


async def set_mark(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    task_id = int(dialog_manager.start_data["task_id"])
    mark = int(dialog_manager.find("r_marks").get_checked())
    _task = await task.get_task(task_id)
    _test = await test.find_test(_task.test_id)

    await task.update_task(task_id, mark=mark)
    await callback.answer(f"Выставлена оценка {mark}", show_alert=True)
    await callback.bot.send_message(_task.user_id, f"Получена оценка {mark} за тест \"{_test.test_name}\"")
    await upd.update_tasks_list()
