from aiogram.filters.state import StatesGroup, State


class AdminMenuStates(StatesGroup):
    main = State()

    tests_management = State()
    solvers_management = State()
    change_time = State()

    add_new_test = State()
    write_name = State()
    write_cost = State()

    add_solver = State()
    remove_solver = State()


class TestMenuStates(StatesGroup):
    main = State()
    change_name = State()
    change_cost = State()

class ManageMenuStates(StatesGroup):
    main = State()