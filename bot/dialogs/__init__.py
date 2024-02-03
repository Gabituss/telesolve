from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs
from bot.dialogs.user import dialogs as user_dialogs
from bot.dialogs.admin import dialogs as admin_dialogs

from aiogram_dialog.tools import render_preview


def setup(dp: Dispatcher):
    dp.include_router(user_dialogs.menu_dialog)
    dp.include_router(user_dialogs.order_process_dialog)
    dp.include_router(user_dialogs.change_task_data_dialog)

    dp.include_router(admin_dialogs.menu_dialog)
    dp.include_router(admin_dialogs.test_dialog)
    dp.include_router(admin_dialogs.manage_dialog)

    setup_dialogs(dp)
