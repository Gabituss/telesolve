from aiogram_dialog import Dialog

from bot.dialogs.user.windows import *

menu_dialog = Dialog(
    menu_window,
    tests_window,
    tasks_window,
)

order_process_dialog = Dialog(
    order_info_window,
    write_data_window,
    write_full_name_window,
    write_deadline_date_window,
    write_deadline_time_window,
    payments_window,
    login_data_info_window,
    write_login_window,
    write_password_window
)

change_task_data_dialog = Dialog(
    task_changer_main_window,
    task_changer_write_login_window,
    task_changer_write_password_window
)
