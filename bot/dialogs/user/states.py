from aiogram.filters.state import StatesGroup, State


class UserMenuStates(StatesGroup):
    main = State()
    select_test = State()

    select_task = State()


class AdminMenuStates(StatesGroup):
    main = State()


class OrderMenuStates(StatesGroup):
    info = State()
    write_data = State()
    write_full_name = State()
    write_deadline_date = State()
    write_deadline_time = State()
    payment = State()

    write_login_data = State()
    write_login = State()
    write_password = State()
