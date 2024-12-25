import uuid

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
from base import int_pk, str_uniq

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[EmailStr] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
