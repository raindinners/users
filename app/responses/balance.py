from __future__ import annotations

import datetime

from schema import ApplicationSchema


class BalanceResponse(ApplicationSchema):
    id: int
    balance: int
    bonus_time: datetime.datetime
