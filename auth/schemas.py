from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class RegisterResponce(BaseModel):
    email: EmailStr
    password: str
    access_token: str