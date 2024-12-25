import uuid
from datetime import datetime

from sqlalchemy import func
from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import mapped_column

int_pk = Annotated[UUID, mapped_column(default=uuid.uuid4, primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]