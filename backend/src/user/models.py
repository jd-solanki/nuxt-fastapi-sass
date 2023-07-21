from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.db import Base


class TableInsertMeta:
    # `nullable=False` enforces there shouldn't be `null` value even if we explicitly/accidentally try to
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )


class User(Base, TableInsertMeta):
    __tablename__ = "users"

    # `id` column will be indexed by default as it is the primary key
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, index=True)

    # recommended email str length is 254
    email: Mapped[str] = mapped_column(String(254), nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(), nullable=False)
