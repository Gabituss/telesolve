from aiogram.filters import BaseFilter
from aiogram.types import Message

from datetime import time


def process_time(_time):
    _time = _time.replace(".", ":")
    _time = _time.replace("-", ":")

    if len(_time) <= 4:
        _time = "0" + _time

    return _time


class TimeFilter():
    def __init__(self):
        pass

    async def __call__(self, text: str):
        _time = process_time(text)

        try:
            time.fromisoformat(_time)
            return True
        except ValueError:
            return False
