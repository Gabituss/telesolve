import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select, ScrollingGroup, Radio
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.text import Const, Format, Jinja

from bot.dialogs.admin.states import AdminMenuStates, TestMenuStates, ManageMenuStates
from bot.dialogs.admin import getters
from bot.dialogs.admin import handlers

from magic_filter import F

menu_window = Window(
    Const("Меню"),
    SwitchTo(Const("Менеджмент опций"), id="tests_btn", state=AdminMenuStates.tests_management),
    SwitchTo(Const("Менеджмент решал"), id="solvers_btn", state=AdminMenuStates.solvers_management),
    SwitchTo(Const("Изменить время работы"), id="change_btn", state=AdminMenuStates.change_time),
    state=AdminMenuStates.main
)

tests_management_menu_window = Window(
    Const("Менеджмент опций"),
    SwitchTo(Const("Добавить новую"), id="add_btn", state=AdminMenuStates.add_new_test),
    ScrollingGroup(
        Select(
            text=Format("{item.test_name} — {item.test_cost}₽"),
            id="test_list",
            items="tests",
            item_id_getter=lambda _test: str(_test.test_id),
            on_click=handlers.select_test,
        ),
        width=1,
        height=8,
        hide_on_single_page=True,
        id="group",
    ),
    SwitchTo(Const("Назад"), id="back_btn", state=AdminMenuStates.main),
    state=AdminMenuStates.tests_management,
    getter=getters.tests_list_getter,
)

test_adding_window = Window(
    Format(
        "Данные по тесту:\n"
        "Название: {name}\n"
        "Цена: {cost}\n"
    ),
    SwitchTo(Format("{name_btn}"), id="name_btn", state=AdminMenuStates.write_name),
    SwitchTo(Format("{cost_btn}"), id="cost_btn", state=AdminMenuStates.write_cost),
    Button(Format("Добавить"), on_click=handlers.create_test, id="create_btn", when=F["all_filled"]),
    SwitchTo(Const("Назад"), id="back_btn", on_click=handlers.clear_order_data, state=AdminMenuStates.tests_management),
    getter=getters.current_test_data_getter,
    state=AdminMenuStates.add_new_test,
)

write_name_window = Window(
    Format("Введите название"),
    SwitchTo(Const("Назад"), id="back", state=AdminMenuStates.add_new_test),
    TextInput(id="name_input", on_success=handlers.write_name),
    state=AdminMenuStates.write_name
)

write_cost_window = Window(
    Format("Введите цену"),
    SwitchTo(Const("Назад"), id="back", state=AdminMenuStates.add_new_test),
    TextInput(id="cost_input", on_success=handlers.write_cost),
    state=AdminMenuStates.write_cost
)

test_preview_window = Window(
    Format(
        "Выбранный тест:\n"
        "Название: {name}\n"
        "Цена: {cost}\n"
    ),
    SwitchTo(Format("Изменить название"), id="name", state=TestMenuStates.change_name),
    SwitchTo(Format("Изменить цену"), id="cost", state=TestMenuStates.change_cost),
    Button(Format("Удалить"), id="delete", on_click=handlers.delete),
    Button(Format("Назад"), id='back', on_click=handlers.go_back),
    state=TestMenuStates.main,
    getter=getters.test_data_getter,
)

change_name_window = Window(
    Format("Введите имя"),
    SwitchTo(Const("Назад"), id='back', state=TestMenuStates.main),
    TextInput(id="name_input", on_success=handlers.change_test_name),
    state=TestMenuStates.change_name
)

change_cost_window = Window(
    Format("Введите цену"),
    SwitchTo(Const("Назад"), id='back', state=TestMenuStates.main),
    TextInput(id="cost_input", on_success=handlers.change_test_cost),
    state=TestMenuStates.change_cost
)

solvers_menu_window = Window(
    Format("Менеджмент решал"),
    SwitchTo(Const("Добавить решалу"), id='add', state=AdminMenuStates.add_solver),
    SwitchTo(Const("Удалить решалу"), id='remove', state=AdminMenuStates.remove_solver),
    SwitchTo(Const("Назад"), id='back', state=AdminMenuStates.main),
    state=AdminMenuStates.solvers_management
)

add_solver_window = Window(
    Format("Введите id решалы"),
    SwitchTo(Const("Назад"), id='back', state=TestMenuStates.main),
    TextInput(id="solver_add_input", on_success=handlers.add_solver),
    state=AdminMenuStates.add_solver
)

remove_solver_window = Window(
    Format("Введите id решалы"),
    SwitchTo(Const("Назад"), id='back', state=TestMenuStates.main),
    TextInput(id="solver_remove_input", on_success=handlers.remove_solver),
    state=AdminMenuStates.remove_solver
)

manage_main_window = Window(
    Format(
        "Менеджмент теста\n"
        "<b>Название теста</b>: {test_name}\n"
        "<b>Статус</b>: {status}\n"
        "<b>Оценка</b>: {mark}\n"
        "<b>Заказчик</b>: {full_name} [@{username}]\n"
        "<b>Дедлайн</b>: {deadline}\n"
        "<b>Логин</b>: <code>{login}</code>\n"
        "<b>Пароль</b>: <code>{password}</code>\n"
    ),
    Button(Const("Начать выполнение"), id="start", on_click=handlers.start_solving_task, when=F["not_started"]),
    Button(Const("Выбери оценку"), id="info", when=F["started"]),
    Radio(
        Format("🔘 {item[0]}"),
        Format("⚪️ {item[0]}"),
        id="r_marks",
        item_id_getter=operator.itemgetter(1),
        items="marks",
        when=F["started"],
    ),
    Button(Const("Выставить оценку"), on_click=handlers.set_mark, id="set_mark", when=F["show_send"]),
    Button(Const("Выйти"), id="back", on_click=handlers.go_back),
    getter=getters.task_data_getter,
    state=ManageMenuStates.main
)

change_work_time_window = Window(
    Const("Введи время работы бота например: \"6:00-8:30\" или \"10:45-18:00\""),
    SwitchTo(Const("Назад"), id='back', state=TestMenuStates.main),
    TextInput(id="time_input", on_success=handlers.update_time),
    state=AdminMenuStates.change_time
)
