from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from fastapi import Request


engine = create_async_engine(settings.POSTGRES_URL, future=True, echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, )
