from __future__ import annotations


class ApplicationError(Exception):
    ...


class TelegramAuthorizationFailed(ApplicationError):
    ...
