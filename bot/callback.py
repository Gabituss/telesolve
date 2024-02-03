from typing import Optional
from aiogram.filters.callback_data import CallbackData


class ApproveCallbackFactory(CallbackData, prefix="approve"):
    value: Optional[int] = None

class DeclineCallbackFactory(CallbackData, prefix="decline"):
    value: Optional[int] = None