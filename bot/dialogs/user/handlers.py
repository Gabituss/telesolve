from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from aiogram_dialog import ShowMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.dialogs.user.states import OrderMenuStates, UpdateTaskMenuStates
from bot.controllers import test, task, user, solver
from bot.dialogs.user import getters
from bot.callback import ApproveCallbackFactory, DeclineCallbackFactory

from bot.dialogs.user.filters import TimeFilter, process_time

from typing import Any
from loguru import logger
from datetime import date, datetime

import config
from bot.worksheet import Updater

upd = Updater("token.json")


async def setup_user_id(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(user_id=callback.from_user.id)


async def on_test_selected(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, selected_item: str):
    _test = await test.find_test(int(selected_item))

    now = datetime.now().time()
    start, end = await user.get_time_deltas()

    if start <= now <= end:

        await dialog_manager.start(OrderMenuStates.info, data={
            "user_id": callback.from_user.id,
            "selected_id": int(selected_item),
        })
    else:
        await callback.answer("Мы сейчас не принимаем заказы 🙁", show_alert=True)


async def on_task_selected(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, selected_item: str):
    _task = await task.get_task(int(selected_item))
    await dialog_manager.start(UpdateTaskMenuStates.main, data={"task_id": _task.task_id})


async def go_back(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await dialog_manager.done()


async def clear_order_data(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    dialog_manager.dialog_data.clear()


async def full_name_input_success(event, widget, dialog_manager: DialogManager, *_):
    full_name = dialog_manager.find("full_name_input").get_value()
    dialog_manager.dialog_data.update(full_name=full_name)
    await dialog_manager.switch_to(OrderMenuStates.write_data)


async def deadline_time_input_success(event, widget, dialog_manager: DialogManager, *_):
    deadline_time = dialog_manager.find("deadline_time_input").get_value()

    if not await TimeFilter()(deadline_time):
        logger.info(f"User {event.from_user.id} [@{event.from_user.username}] wrote wrong date")
        await event.answer("Неправильный формат времени :(")
    else:
        logger.info(f"User {event.from_user.id} [@{event.from_user.username}] selected time")
        dialog_manager.dialog_data.update(deadline_time=process_time(deadline_time))

    await dialog_manager.switch_to(OrderMenuStates.write_data)


async def select_date(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, selected_date: date):
    if selected_date < date.today():
        logger.info(f"User {callback.from_user.id} [@{callback.from_user.username}] selected old date")
        return

    logger.info(f"User {callback.from_user.id} [@{callback.from_user.username}] selected date")
    dialog_manager.dialog_data.update(deadline_date=selected_date.isoformat())
    await dialog_manager.switch_to(OrderMenuStates.write_data)


async def receipt_handler(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    logger.info(f"Received receipt from {message.from_user.id} [@{message.from_user.username}]")
    dialog_manager.dialog_data.update(receipt_file_id=message.document.file_id)

    await dialog_manager.switch_to(OrderMenuStates.write_login_data)


async def receipt_handler_wrong_type(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    logger.info(f"Received wrong file type of receipt from {message.from_user.id} [@{message.from_user.username}]")

    await message.answer("Ой... Кажется вы отправили чек не в формате файла, попробуйте снова")


async def login_handler(event, widget, dialog_manager: DialogManager, *_):
    login = dialog_manager.find("login").get_value()
    dialog_manager.dialog_data.update(login=login)

    await dialog_manager.switch_to(OrderMenuStates.write_login_data)


async def password_handler(event, widget, dialog_manager: DialogManager, *_):
    password = dialog_manager.find("password").get_value()
    dialog_manager.dialog_data.update(password=password)

    await dialog_manager.switch_to(OrderMenuStates.write_login_data)


async def create_task_handler(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    data = await getters.current_order_data_getter(dialog_manager)
    task_id = await task.get_new_id()

    full_name = dialog_manager.dialog_data.get("full_name")

    await user.update_user(callback.from_user.id, full_name=full_name)
    _task = await task.create_task(
        task_id=task_id,
        user_id=dialog_manager.start_data.get("user_id"),
        test_id=dialog_manager.start_data.get("selected_id"),

        full_name=full_name,
        deadline=f'{data.get("deadline_date")} {data.get("deadline_time")}',
        login=data.get("login"),
        password=data.get("password"),

        mark=-1,
        approved=0,
        hidden=False
    )
    _test = await test.find_test(dialog_manager.start_data.get("selected_id"))
    logger.info(f"Created task {_task.task_id} {_task.user_id}")
    await callback.answer(f"❤Благодарим Вас за покупку❤️\n\n✍🏼Тест будет выполнен до конца дедлайна✍🏼\n",
                          show_alert=True)

    for _solver in await solver.get_solvers():
        if _solver.user_id != config.OWNER:
            await callback.bot.send_message(
                _solver.user_id,
                f"Получен заказ на тест \"{_test.test_name}\""
            )
        else:
            keyboard = InlineKeyboardBuilder()
            keyboard.button(text="Подтвердить", callback_data=ApproveCallbackFactory(value=_task.task_id))
            keyboard.button(text="Отклонить", callback_data=DeclineCallbackFactory(value=_task.task_id))

            await callback.bot.send_document(
                chat_id=config.OWNER,
                document=dialog_manager.dialog_data["receipt_file_id"],
                caption=f'Заказ от {full_name} по "{_test.test_name} за {_test.test_cost}₽"',
                reply_markup=keyboard.as_markup()
            )
            pass

    await dialog_manager.done()
    await upd.update_tasks_list()


async def change_login_handler(event, widget, dialog_manager: DialogManager, *_):
    login = dialog_manager.find("login_input").get_value()
    task_id = dialog_manager.start_data["task_id"]

    await task.update_task(task_id, login=login)
    await dialog_manager.switch_to(UpdateTaskMenuStates.main)
    await upd.update_tasks_list()


async def change_password_handler(event, widget, dialog_manager: DialogManager, *_):
    password = dialog_manager.find("password_input").get_value()
    task_id = dialog_manager.start_data["task_id"]

    await task.update_task(task_id, password=password)
    await dialog_manager.switch_to(UpdateTaskMenuStates.main)
    await upd.update_tasks_list()
