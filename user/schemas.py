from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserInfo(BaseModel):
    email: EmailStr
    created_at: datetime
    updated_at: datetime
