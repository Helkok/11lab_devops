from fastapi import APIRouter, Depends
from starlette.requests import Request

from user.model import User
from user.schemas import UserInfo
from user.utils import UserUtils
from utils import get_current_user

router = APIRouter()


@router.get("/")
async def get_all_users(request: Request):
    return await UserUtils.get_all_users_from_db(request.state.db)


@router.get("/me")
async def get_me(user_data: User = Depends(get_current_user)) -> UserInfo:
    return UserInfo(email = user_data.email,
                    created_at = user_data.created_at,
                    updated_at = user_data.updated_at)



@router.delete("/delete")
async def delete_user(email: str, request: Request):
    return await UserUtils.delete_user(email, request.state.db)
