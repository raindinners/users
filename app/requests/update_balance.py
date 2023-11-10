from __future__ import annotations

from schema import ApplicationSchema


class UpdateBalanceRequest(ApplicationSchema):
    user_id: int
    balance: int
    bot_token: str
