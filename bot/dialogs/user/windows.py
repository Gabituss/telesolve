from magic_filter import F

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select, ScrollingGroup
from aiogram_dialog.widgets.input import TextInput, MessageInput

from aiogram_dialog.widgets.text import Const, Format, Jinja

from bot.dialogs.user.states import UserMenuStates, OrderMenuStates

from bot.dialogs.user import getters, handlers

from bot.dialogs.user.widgets import CustomCalendar

from aiogram.types import ContentType

menu_window = Window(
    Const("MENU"),
    SwitchTo(Const("Order test"), state=UserMenuStates.select_test, on_click=handlers.setup_user_id,
             id="switch_to_tests"),
    SwitchTo(Const("My tasks"), state=UserMenuStates.select_task, on_click=handlers.setup_user_id,
             id="switch_to_tasks"),
    state=UserMenuStates.main,
)

tests_window = Window(
    Const("Here you can order some tests"),
    ScrollingGroup(
        Select(
            text=Format("{item.test_name} {item.test_cost}"),
            id="test_list",
            items="tests",
            item_id_getter=getters.test_id_getter,
            on_click=handlers.on_test_selected,
        ),
        id="test_selector",
        width=1,
        height=6,
        hide_on_single_page=True
    ),
    SwitchTo(Const("Back"), state=UserMenuStates.main, id="switch"),
    state=UserMenuStates.select_test,
    getter=getters.tests_list_getter,
)

tasks_window = Window(
    Const("Your tests"),
    ScrollingGroup(
        Select(
            text=Jinja("{{ data['names'][item.task_id] }}"),
            id="tasks_list",
            items="tasks",
            item_id_getter=getters.task_id_getter,
        ),
        id="task_selector",
        width=1,
        height=6,
        hide_on_single_page=True
    ),
    SwitchTo(Const("Back"), state=UserMenuStates.main, id="switch"),
    state=UserMenuStates.select_task,
    getter=getters.tasks_list_getter,
)

# region Collect basic data
order_info_window = Window(
    Format(
        "You selected test id={test_id}\n"
        "Test name is {test_name}\n"
        "Test cost is {test_cost}\n"
    ),
    SwitchTo(Const("Continue"), id="next", state=OrderMenuStates.write_data),
    Button(Const("Back"), id="back", on_click=handlers.go_back),
    getter=getters.test_info_getter,
    state=OrderMenuStates.info,
)

write_data_window = Window(
    Format(
        "You selected \"{test_name}\" test with cost {test_cost}\n"
        "Please, fill data:\n"
        "Full name: {full_name}\n"
        "Deadline date: {deadline_date}\n"
        "Deadline time: {deadline_time}\n"
    ),
    SwitchTo(Format("{full_name_btn_text}"), id="name_btn", state=OrderMenuStates.write_full_name),
    SwitchTo(Format("{deadline_date_btn_text}"), id="deadline_date_btn", state=OrderMenuStates.write_deadline_date),
    SwitchTo(Format("{deadline_time_btn_text}"), id="deadline_time_btn", state=OrderMenuStates.write_deadline_time),
    SwitchTo(Format("Go to payment"), id="payment_btn", state=OrderMenuStates.payment, when=F["all_filled"]),
    SwitchTo(Const("Back"), id="back_btn", state=OrderMenuStates.info, on_click=handlers.clear_order_data),
    getter=getters.current_order_data_getter,
    state=OrderMenuStates.write_data
)

write_full_name_window = Window(
    Format("Write your full name"),
    SwitchTo(Const("Back"), id="back_btn", state=OrderMenuStates.write_data),
    TextInput(id="full_name_input", on_success=handlers.full_name_input_success),
    state=OrderMenuStates.write_full_name
)

write_deadline_date_window = Window(
    Format("Select deadline date"),
    CustomCalendar(id="calendar", on_click=handlers.select_date),
    SwitchTo(Const("Back"), id="back_btn", state=OrderMenuStates.write_data),
    state=OrderMenuStates.write_deadline_date
)

write_deadline_time_window = Window(
    Format("Write deadline time"),
    SwitchTo(Const("Back"), id="back_btn", state=OrderMenuStates.write_data),
    TextInput(id="deadline_time_input", on_success=handlers.deadline_time_input_success),
    state=OrderMenuStates.write_deadline_time
)

payments_window = Window(
    Format("Please pay for test and send receipt as a file"),
    MessageInput(handlers.receipt_handler, content_types=[ContentType.DOCUMENT]),
    MessageInput(handlers.receipt_handler_wrong_type),
    state=OrderMenuStates.payment
)
# endregion

# region Collect login data
login_data_info_window = Window(
    Format(
        "Thanks for the purchase, now write login data:\n"
        "Login: {login}\n"
        "Password: {password}\n"
    ),
    SwitchTo(Format("{write_login_btn_text}"), id="login_btn", state=OrderMenuStates.write_login),
    SwitchTo(Format("{write_password_btn_text}"), id="password_btn", state=OrderMenuStates.write_password),
    Button(Const("Finish"), on_click=handlers.create_task_handler, id="finish", when=F["all_login_data_filled"]),
    getter=getters.current_order_data_getter,
    state=OrderMenuStates.write_login_data
)

write_login_window = Window(
    Format("Write your login"),
    TextInput(on_success=handlers.login_handler, id="login"),
    SwitchTo(Const("Back"), id="back", state=OrderMenuStates.write_login_data),
    state=OrderMenuStates.write_login,
)

write_password_window = Window(
    Format("Write your password"),
    TextInput(on_success=handlers.password_handler, id="password"),
    SwitchTo(Const("Back"), id="back", state=OrderMenuStates.write_login_data),
    state=OrderMenuStates.write_password
)
# endregion
