from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field

from schema import ApplicationSchema

if TYPE_CHECKING:
    from .balance import BalanceResponse


class UserResponse(ApplicationSchema):
    id: int
    telegram_id: int
    username: Optional[str] = Field(default=None, max_length=32)
    first_name: str = Field(max_length=30)
    last_name: Optional[str] = Field(default=None, max_length=30)
    full_name: str
    balance: Optional[BalanceResponse] = None
