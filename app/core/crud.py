from __future__ import annotations

from corecrud import CRUD as CCRUD  # noqa
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from orm import BalanceModel, UserModel


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class CRUD:
    balances: CCRUD[BalanceModel] = CCRUD(BalanceModel)
    users: CCRUD[UserModel] = CCRUD(UserModel)


crud = CRUD()
