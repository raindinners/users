from __future__ import annotations

from typing import Optional

from pydantic import Field

from schema import ApplicationSchema


class TelegramAuthRequest(ApplicationSchema):
    id: int = Field(alias="telegram_id")
    first_name: str = Field(max_length=30)
    last_name: Optional[str] = Field(default=None, max_length=30)
    username: Optional[str] = Field(default=None, max_length=32)
    auth_date: int
    hash: str
