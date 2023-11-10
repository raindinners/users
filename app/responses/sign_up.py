from __future__ import annotations

from schema import ApplicationSchema


class SignUpResponse(ApplicationSchema):
    access_token: str
