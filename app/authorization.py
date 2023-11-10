from __future__ import annotations

from typing import Optional

import jwt
from fastapi.exceptions import HTTPException
from starlette import status

from core.settings import auth_settings


def get_user_id(access_token: Optional[str] = None) -> int:
    return jwt.decode(
        jwt=access_token,
        key=auth_settings.SECRET_KEY,
        algorithms=[auth_settings.ALGORITHM],
    )["sub"]


def get_user_id_failed(access_token: Optional[str] = None) -> int:
    try:
        return get_user_id(access_token=access_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="AUTHORIZATION_FAILED",
        )
