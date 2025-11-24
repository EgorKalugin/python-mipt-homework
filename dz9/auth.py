import uuid

from dz9.main import Base
from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )
    username: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )
    password: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
