from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, ClassVar, Final, Optional

from sqlalchemy.orm import Mapped, relationship

from .core import ORMModel, types

if TYPE_CHECKING:
    from .user import UserModel


class BalanceModel(ORMModel):
    BONUS: Final[ClassVar[int]] = 15000
    BONUS_EVERY_HOURS: Final[ClassVar[int]] = 4

    balance: Mapped[types.BigInt]
    bonus_time: Mapped[Optional[datetime.datetime]]

    user_id: Mapped[types.User]
    user: Mapped[Optional[UserModel]] = relationship(back_populates="balance")

    def is_bonus(self) -> bool:
        if not self.bonus_time:
            return True

        return (
            self.bonus_time + datetime.timedelta(hours=BalanceModel.BONUS_EVERY_HOURS)
            >= datetime.datetime.now()
        )  # noqa
