from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from config import settings
from user.model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

class JWT:

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MIN)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except JWTError:
            raise ValueError("Invalid token or token has expired")

security = HTTPBearer()


async def get_current_user(request: Request, token: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        # Извлекаем сам токен из credentials
        token_str = token.credentials  # token.credentials содержит сам JWT токен

        # Декодируем токен
        payload = jwt.decode(token_str, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # Получаем сессию из request.state.db
        db: AsyncSession = request.state.db

        # Выполняем асинхронный запрос для получения пользователя
        result = await db.execute(select(User).filter(User.email == user_email))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")




