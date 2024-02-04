import pygsheets
from pygsheets.exceptions import WorksheetNotFound
from googleapiclient.errors import HttpError

from functools import cmp_to_key
from bot.models import Task, Test
from bot.controllers import user, task, test

from datetime import datetime
from loguru import logger


def compare(l: Task, r: Task):
    l_val = (
        [0, -1, 1][l.approved],
        datetime.strptime(l.deadline, '%Y-%m-%d %H:%M'),
        min(l.mark, 1)
    )

    r_val = (
        [0, -1, 1][r.approved],
        datetime.strptime(r.deadline, '%Y-%m-%d %H:%M'),
        min(r.mark, 1)
    )

    if l_val == r_val:
        return 0

    if l_val[0] == r_val[0]:
        if l_val[2] == r_val[2]:
            return -1 if l_val[1] < r_val[1] else 1
        else:
            return -1 if l_val[2] < r_val[2] else 1
    else:
        return -1 if l_val[0] > r_val[0] else 1


def check(l: Task):
    return not l.hidden


async def convert(_task: Task):
    _user = await user.get_user(_task.user_id)
    _test = await test.find_test(_task.test_id)
    return [
        _test.test_name,
        _task.deadline,
        f"{_task.full_name} [@{_user.username}]",
        _task.login,
        _task.password,
        _task.mark,
        _task.approved,
        f"/manage {_task.task_id}",
    ]


async def add_tasks(tasks, sheet, start):
    if len(tasks) <= 0:
        return

    vals = [await convert(_task) for _task in tasks]
    sheet.update_values(f"A{start}", vals)


def clear(sheet):
    sheet.clear(fields="*")


class Updater:
    def __init__(self, path):
        self.client = pygsheets.authorize(service_file=path)
        self.sh = self.client.open("tasks")

    async def create_worksheet(self, tp):
        wks = self.sh.add_worksheet(tp, rows=2000)
        wks.add_conditional_formatting('G2', f'G1500', 'NUMBER_BETWEEN',
                                       {'background_color': {'green': 1}},
                                       ['2', '2'])
        wks.add_conditional_formatting('G2', f'G1500', 'NUMBER_BETWEEN',
                                       {'background_color': {'green': 1, 'red': 1}},
                                       ['0', '0'])
        wks.add_conditional_formatting('G2', f'G1500', 'NUMBER_BETWEEN',
                                       {'background_color': {'red': 1}},
                                       ['1', '1'])
        wks.add_conditional_formatting('F2', f'F1500', 'NUMBER_BETWEEN',
                                       {'background_color': {'green': 1}},
                                       ['1', '1000'])
        wks.add_conditional_formatting('F2', f'F1500', 'NUMBER_BETWEEN',
                                       {'background_color': {'green': 1, 'red': 1}},
                                       ['0', '0'])
        wks.add_conditional_formatting('F2', f'F1500', 'NUMBER_BETWEEN',
                                       {'background_color': {'red': 1}},
                                       ['-1', '-1'])

        return wks

    async def update_tasks_list(self):
        tasks = await task.get_all_tasks(show_hidden=False)
        tasks = sorted(tasks, key=cmp_to_key(compare))

        types = dict()
        for _task in tasks:
            _test = await test.find_test(_task.test_id)
            if not check(_task):
                continue

            types["главное"] = types.get("главное", []) + [_task]
            types[_test.test_name.split()[0]] = types.get(_test.test_name.split()[0], []) + [_task]

        for _test in (await test.get_all_tests_names()) + ["главное"]:
            tp = _test.split()[0]
            tasks = types.get(tp, [])

            try:
                wks = self.sh.worksheet_by_title(tp)
            except WorksheetNotFound or HttpError:
                if len(tasks) != 0:
                    wks = await self.create_worksheet(tp)
                else:
                    continue

            clear(wks)

            if len(tasks) == 0:
                continue

            wks.update_values('A1', [["Тип теста", "Дедлайн", "ФИО", "Логин", "Пароль", "Оценка", "Подтвержден",
                                      "Команда для менеджмента"]])

            tasks3 = list(filter(lambda t: t.approved == 2 and check(t), tasks))
            tasks2 = list(filter(lambda t: t.approved == 0 and check(t), tasks))
            tasks1 = list(filter(lambda t: t.approved == 1 and check(t), tasks))

            await add_tasks(tasks3, wks, 2)
            await add_tasks(tasks2, wks, 3 + len(tasks3))
            await add_tasks(tasks1, wks, 4 + len(tasks3) + len(tasks2))

            wks.adjust_column_width(1, 10)
