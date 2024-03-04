from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram import F

from bot.handlers.admin.commands import *
from bot.handlers.admin import filters

from bot.controllers import solver, user
from bot.callback import ApproveCallbackFactory, DeclineCallbackFactory


async def setup(dp: Dispatcher):
    await solver.create_solver(1173441935)
    await user.create_user(0, "08:00", "")
    await user.create_user(1, "18:00", "")

    dp.message.register(cmd_start, filters.SolverFilter(), Command("start_admin"))
    dp.message.register(cmd_show_tasks, filters.SolverFilter(), Command("show_tasks"))
    dp.message.register(cmd_manage, filters.SolverFilter(), Command("manage"))
    dp.message.register(cmd_update, filters.SolverFilter(), Command("update"))
    dp.message.register(cmd_hide_tasks, filters.SolverFilter(), Command("clear"))
    dp.message.register(cmd_hide_all_tasks, filters.SolverFilter(), Command("clear_all"))
    dp.message.register(cmd_remove_task, filters.SolverFilter(), Command("remove_task"))

    dp.callback_query.register(cmd_approve_task, ApproveCallbackFactory.filter())
    dp.callback_query.register(cmd_decline_task, DeclineCallbackFactory.filter())
