from __future__ import annotations

from typing import Optional

from schema import ApplicationSchema


class AuthRequest(ApplicationSchema):
    access_token: Optional[str] = None
    user_id: Optional[int] = None
