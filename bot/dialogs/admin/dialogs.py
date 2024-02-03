from aiogram_dialog import Dialog

from bot.dialogs.admin.windows import *

menu_dialog = Dialog(
    menu_window,
    tests_management_menu_window,
    test_adding_window,
    write_name_window,
    write_cost_window,
    solvers_menu_window,
    add_solver_window,
    remove_solver_window,
    change_work_time_window
)

test_dialog = Dialog(
    test_preview_window,
    change_name_window,
    change_cost_window
)

manage_dialog = Dialog(
    manage_main_window
)