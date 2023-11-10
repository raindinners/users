from __future__ import annotations

import datetime
from typing import Optional

from schema import ApplicationSchema


class BalanceResponse(ApplicationSchema):
    id: int
    balance: int
    next_time_bonus: Optional[datetime.datetime] = None
