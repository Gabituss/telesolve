from magic_filter import F

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Select, ScrollingGroup, Url
from aiogram_dialog.widgets.input import TextInput, MessageInput

from aiogram_dialog.widgets.text import Const, Format, Jinja

from bot.dialogs.user.states import UserMenuStates, OrderMenuStates, UpdateTaskMenuStates

from bot.dialogs.user import getters, handlers

from bot.dialogs.user.widgets import CustomCalendar

from aiogram.types import ContentType

menu_window = Window(
    Const("Меню"),
    SwitchTo(
        Const("💎 Заказать тест 💎"),
        state=UserMenuStates.select_test,
        on_click=handlers.setup_user_id,
        id="switch_to_tests"
    ),
    SwitchTo(
        Const("⏳ Мои заказы ⏳"),
        state=UserMenuStates.select_task,
        on_click=handlers.setup_user_id,
        id="switch_to_tasks"
    ),
    Url(Const("✏️ Менеджер ✏️"), Const('https://t.me/MANAGER_MTTS')),
    Url(Const("📕️ Канал 📕️"), Const('https://t.me/MGMSU_TestTech_Squad')),
    state=UserMenuStates.main,
)

tests_window = Window(
    Const("Здесь Вы можете выбрать тест, который нужно решить 📝\n"
          "В случае если вашего теста нет в списке - напишите менеджеру для его добавления 🔎"),
    ScrollingGroup(
        Select(
            text=Format("{item.test_name} — {item.test_cost}₽"),
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
    SwitchTo(Const("⬅️ Назад"), state=UserMenuStates.main, id="switch"),
    state=UserMenuStates.select_test,
    getter=getters.tests_list_getter,
)

# region Collect basic data
order_info_window = Window(
    Format(
        "Название теста: {test_name}\n"
        "<b>Цена за тест</b>: {test_cost}₽\n"
    ),
    SwitchTo(Const("Дальше ➡️"), id="next", state=OrderMenuStates.write_data),
    Button(Const("⬅️ Назад"), id="back", on_click=handlers.go_back),
    getter=getters.test_info_getter,
    state=OrderMenuStates.info,
)

write_data_window = Window(
    Format(
        "Вы выбрали тест \"{test_name}\" за {test_cost}₽\n"
        "Пожалуйста, заполните данные:\n"
        "<b>ФИО</b>: {full_name}\n"
        "<b>Дата дедлайна</b>: {deadline_date}\n"
        "<b>Время дедлайна</b>: {deadline_time}\n"
    ),
    SwitchTo(Format("{full_name_btn_text}"), id="name_btn", state=OrderMenuStates.write_full_name),
    SwitchTo(Format("{deadline_date_btn_text}"), id="deadline_date_btn", state=OrderMenuStates.write_deadline_date),
    SwitchTo(Format("{deadline_time_btn_text}"), id="deadline_time_btn", state=OrderMenuStates.write_deadline_time),
    SwitchTo(Format("Перейти к оплате ➡️"), id="payment_btn", state=OrderMenuStates.payment, when=F["all_filled"]),
    SwitchTo(Const("⬅️ Назад"), id="back_btn", state=OrderMenuStates.info, on_click=handlers.clear_order_data),
    getter=getters.current_order_data_getter,
    state=OrderMenuStates.write_data
)

write_full_name_window = Window(
    Format("Введите ФИО"),
    SwitchTo(Const("⬅️ Назад"), id="back_btn", state=OrderMenuStates.write_data),
    TextInput(id="full_name_input", on_success=handlers.full_name_input_success),
    state=OrderMenuStates.write_full_name
)

write_deadline_date_window = Window(
    Format("Выберите дату дедлайна"),
    CustomCalendar(id="calendar", on_click=handlers.select_date),
    SwitchTo(Const("⬅️ Назад"), id="back_btn", state=OrderMenuStates.write_data),
    state=OrderMenuStates.write_deadline_date
)

write_deadline_time_window = Window(
    Format("Введите время дедлайна в формате час:минута, например \"16:30\" или \"09:30\" (МСК)"),
    SwitchTo(Const("⬅️ Назад"), id="back_btn", state=OrderMenuStates.write_data),
    TextInput(id="deadline_time_input", on_success=handlers.deadline_time_input_success),
    state=OrderMenuStates.write_deadline_time
)

payments_window = Window(
    Jinja(
        "К оплате <b>{{test_cost}}₽</b>\n"
        "🧾 Переведите деньги по СБП на <b>+79859401854 Тинькофф</b> и <b>отправьте файлом</b> чек об оплате 🧾\n\n"
        "👩🏻‍💼 Заказ будет ждать подтвердения менеджера 👩🏻‍💼\n\n"
        "🔔 Как только он будет подтвержден, Вам придет уведомление 🔔\n\n"
        "⌛️ Если в течение одного часа не будет подтверждения, обратитесь к <a href=\"https://t.me/MANAGER_MTTS\">менеджеру</a> ⌛️\n\n"
        "🤔 В случае возникновения вопросов обратитесь к менеджеру 🤔"
    ),
    MessageInput(handlers.receipt_handler, content_types=[ContentType.DOCUMENT]),
    MessageInput(handlers.receipt_handler_wrong_type),
    getter=getters.current_order_data_getter,
    state=OrderMenuStates.payment
)
# endregion

# region Collect login data
login_data_info_window = Window(
    Format(
        "Спасибо за покупку, введите данные для входа:\n"
        "<b>Логин</b>: {login}\n"
        "<b>Пароль</b>: {password}\n"
    ),
    SwitchTo(Format("{write_login_btn_text}"), id="login_btn", state=OrderMenuStates.write_login),
    SwitchTo(Format("{write_password_btn_text}"), id="password_btn", state=OrderMenuStates.write_password),
    Button(Const("Заказать тест ✅"), on_click=handlers.create_task_handler, id="finish", when=F["all_login_data_filled"]),
    getter=getters.current_order_data_getter,
    state=OrderMenuStates.write_login_data
)

write_login_window = Window(
    Format("Введите логин 👨‍💻"),
    TextInput(on_success=handlers.login_handler, id="login"),
    SwitchTo(Const("⬅️ Назад"), id="back", state=OrderMenuStates.write_login_data),
    state=OrderMenuStates.write_login,
)

write_password_window = Window(
    Format("Введите пароль 🔑"),
    TextInput(on_success=handlers.password_handler, id="password"),
    SwitchTo(Const("⬅️ Назад"), id="back", state=OrderMenuStates.write_login_data),
    state=OrderMenuStates.write_password
)
# endregion

tasks_window = Window(
    Const("Здесь Вы можете ознакомиться с Вашими заказами 🗒"),
    ScrollingGroup(
        Select(
            text=Jinja("{{ data['names'][item.task_id] }}"),
            id="tasks_list",
            items="tasks",
            on_click=handlers.on_task_selected,
            item_id_getter=getters.task_id_getter,
        ),
        id="task_selector",
        width=1,
        height=6,
        hide_on_single_page=True
    ),
    SwitchTo(Const("⬅️ Назад"), state=UserMenuStates.main, id="switch"),
    state=UserMenuStates.select_task,
    getter=getters.tasks_list_getter,
)

task_changer_main_window = Window(
    Format(
        "Выбранный тест:\n"
        "<b>Название теста</b>: {name}\n"
        "<b>Статус</b>: {status}\n"
        "<b>Оценка</b>: {mark}\n"
        "<b>Дедлайн</b>: {deadline}\n"
        "<b>Логин</b>: {login}\n"
        "<b>Пароль</b>: {password}\n"
    ),
    SwitchTo(Const("Изменить логин"), state=UpdateTaskMenuStates.change_login, id="login"),
    SwitchTo(Const("Изменить пароль"), state=UpdateTaskMenuStates.change_password, id="password"),
    Button(Const("⬅️ Назад"), id="back", on_click=handlers.go_back),
    state=UpdateTaskMenuStates.main,
    getter=getters.task_getter
)

task_changer_write_login_window = Window(
    Format("Введите логин"),
    TextInput(on_success=handlers.change_login_handler, id="login_input"),
    SwitchTo(Const("⬅️ Назад"), id="back", state=UpdateTaskMenuStates.main),
    state=UpdateTaskMenuStates.change_login
)

task_changer_write_password_window = Window(
    Format("Введите пароль"),
    TextInput(on_success=handlers.change_password_handler, id="password_input"),
    SwitchTo(Const("⬅️ Назад"), id="back", state=UpdateTaskMenuStates.main),
    state=UpdateTaskMenuStates.change_password
)
