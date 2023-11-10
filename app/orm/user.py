from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .core import ORMModel, types

if TYPE_CHECKING:
    from .balance import BalanceModel


class UserModel(ORMModel):
    telegram_id: Mapped[types.BigInt]
    username: Mapped[Optional[types.String32]] = mapped_column(unique=True, index=True)
    first_name: Mapped[types.String30]
    last_name: Mapped[Optional[types.String30]]

    balance: Mapped[Optional[BalanceModel]] = relationship(back_populates="user")

    @hybrid_property
    def full_name(self) -> types.Text:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"

        return f"{self.first_name}"
