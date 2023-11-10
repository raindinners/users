from sqlalchemy import ForeignKey, types
from sqlalchemy.orm import mapped_column
from typing_extensions import Annotated

BigInt = Annotated[int, mapped_column(types.BIGINT)]

String30 = Annotated[str, mapped_column(types.String(30))]
String32 = Annotated[str, mapped_column(types.String(32))]
Text = Annotated[str, mapped_column(types.Text)]

User = Annotated[int, mapped_column(ForeignKey("user.id"))]
