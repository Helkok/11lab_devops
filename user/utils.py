from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user.model import User
from utils import Hasher


class UserUtils:
    @staticmethod
    async def get_all_users_from_db(session: AsyncSession):
        result = await session.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def add_new_user_in_db(user, session: AsyncSession):
        user = user
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def find_by_email(email, session: AsyncSession):
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def add_user(email: str, password: str, session: AsyncSession):
        existing_user = await UserUtils.find_by_email(email=email, session=session)
        if existing_user:
            raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")

        hashed_password = Hasher.get_password_hash(password)
        new_user = User(email=email, password=hashed_password)

        return await UserUtils.add_new_user_in_db(new_user, session)

    @staticmethod
    async def delete_user(email: str, session:AsyncSession):
        result = await session.execute(select(User).where(User.email==email))
        user = result.scalar_one_or_none()
        await session.delete(user)
        await session.commit()
        return {"message": "User deleted successfully"}




