from __future__ import annotations

from schema import ApplicationSchema


class UserInformationRequest(ApplicationSchema):
    user_id: int
