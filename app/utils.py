from __future__ import annotations

import hashlib
import hmac
import time
from typing import Any, Dict, List, Literal, Optional, Sequence, Union

from exc import TelegramAuthorizationFailed
from requests import TelegramAuthRequest


def verify_telegram_authorization(request: TelegramAuthRequest, bot_token: str) -> None:
    """
    Check if received data from Telegram is real.

    Based on SHA and HMAC algothims.
    Instructions - https://core.telegram.org/widgets/login#checking-authorization
    """

    string = "\n".join(
        [
            f"{key}={value}"
            for key, value in sorted(
                request.model_dump(exclude={"hash"}).items(), key=lambda x: x[0]
            )
        ]
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()

    if time.time() - request.auth_date > 86400:  # greater than 1 day
        raise TelegramAuthorizationFailed("AUTHORIZATION_DATA_OUTDATED")

    hash = hmac.new(secret_key, msg=string.encode(), digestmod=hashlib.sha256).hexdigest()  # noqa

    if hash != request.hash:
        raise TelegramAuthorizationFailed("INVALID_HASH")


def model_rebuild(__all__: Sequence[str], __globals__: Dict[str, Any]) -> None:
    for _entity_name in __all__:
        _entity = __globals__[_entity_name]
        if not hasattr(_entity, "model_rebuild"):
            continue

        _entity.model_rebuild(
            _types_namespace={
                "List": List,
                "Optional": Optional,
                "Union": Union,
                "Literal": Literal,
                **{k: v for k, v in __globals__.items() if k in __all__},
            }
        )
