from __future__ import annotations

from schema import ApplicationSchema


class UpdateBalanceRequest(ApplicationSchema):
    access_token: str
    balance: int
