from loguru import logger

from aiogram import types
from aiogram.filters import CommandObject
from aiogram_dialog import DialogManager, StartMode, ShowMode

import config
from bot.dialogs.user.states import UserMenuStates
from bot.dialogs.admin.states import AdminMenuStates, ManageMenuStates

from bot.controllers import user, test, task
from bot.callback import ApproveCallbackFactory, DeclineCallbackFactory

from bot.worksheet import Updater

import os

upd = Updater("token.json")


async def cmd_start(message: types.Message, command: CommandObject, dialog_manager: DialogManager):
    await dialog_manager.start(AdminMenuStates.main, mode=StartMode.RESET_STACK, show_mode=ShowMode.DELETE_AND_SEND)


async def cmd_update(message: types.Message, command: CommandObject, dialog_manager: DialogManager):
    await upd.update_tasks_list()
    await message.answer("OK")


async def cmd_manage(message: types.Message, command: CommandObject, dialog_manager: DialogManager):
    if command.args is None:
        await message.answer("Не введен id заказа")
        return

    task_id = int(command.args.split(" ", maxsplit=1)[0])
    if not await task.task_exists(task_id):
        await message.answer(f"Такого заказа не существует")
        return

    await dialog_manager.start(ManageMenuStates.main, data={"task_id": task_id})

async def cmd_hide_all_tasks(message: types.Message, command: CommandObject, dialog_manager: DialogManager):
    tasks = await task.get_all_tasks()
    for _task in tasks:
        await task.update_task(_task.task_id, hidden=True)
    await upd.update_tasks_list()
    await message.answer("OK")

async def cmd_hide_tasks(message: types.Message, command: CommandObject, dialog_manager: DialogManager):
    tasks = await task.get_all_tasks()
    for _task in tasks:
        if _task.mark != -1:
            await task.update_task(_task.task_id, hidden=True)

    await upd.update_tasks_list()
    await message.answer("OK")


async def cmd_approve_task(
        callback: types.CallbackQuery,
        callback_data: ApproveCallbackFactory
):
    task_id = callback_data.value
    _task = await task.get_task(task_id)
    _test = await test.find_test(_task.test_id)

    await task.update_task(task_id, approved=2)
    await callback.message.bot.send_message(_task.user_id, text=f"Заказ \"{_test.test_name}\" подтвержден ✅")
    await callback.message.delete()
    await callback.message.bot.send_document(
        chat_id=config.OWNER,
        document=callback.message.document.file_id,
        caption=f"Заказ от {_task.full_name} \"{_test.test_name}\" подтвержден"
    )

    await callback.answer()
    await upd.update_tasks_list()


async def cmd_decline_task(
        callback: types.CallbackQuery,
        callback_data: DeclineCallbackFactory
):
    task_id = callback_data.value
    _task = await task.get_task(task_id)
    _test = await test.find_test(_task.test_id)

    await task.update_task(task_id, approved=1)
    await callback.message.bot.send_message(_task.user_id,
                                            text=f"Заказ \"{_test.test_name}\" отклонен ❌, обратитесь к менеджеру чтобы узнать причину")
    await callback.message.delete()
    await callback.message.bot.send_document(
        chat_id=config.OWNER,
        document=callback.message.document.file_id,
        caption=f"Заказ от {_task.full_name} по тесту \"{_test.test_name}\" отклонен"
    )

    await callback.answer()
    await upd.update_tasks_list()

async def cmd_remove_task(message: types.Message, command: CommandObject, dialog_manager: DialogManager):
    task_id = int(command.args)
   
    
    await task.update_task(task_id, hidden=True)
    await message.answer("OK")
    await upd.update_tasks_list()

async def cmd_show_tasks(message: types.Message, command: CommandObject, dialog_manager: DialogManager):
    tasks = await task.get_all_tasks()
    for _task in tasks:
        _user = await user.get_user(_task.user_id)
        _test = await test.find_test(_task.test_id)
        await message.answer(f"{_task.full_name} [@{_user.username if _user is not None else 'N/A'}]\n"
                             f"test_name={_test.test_name}\n"
                             f"task_id={_task.task_id}\n"
                             f"task_mark={_task.mark}\n"
                             f"approve_status={_task.approved}\n")
