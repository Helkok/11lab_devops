from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from user.utils import UserUtils
from auth.schemas import UserCreate, RegisterResponce
from utils import JWT

router = APIRouter()

@router.post("/register/")
async def register_user(user_data: UserCreate, request: Request) -> RegisterResponce:
    try:
        new_user = await UserUtils.add_user(
            email=user_data.email,
            password=user_data.password,
            session=request.state.db
        )
        access_token = JWT.create_access_token(data={"sub": new_user.email})
        return RegisterResponce(
            email=new_user.email,
            password=new_user.password,
            access_token=access_token
        )

    except HTTPException as e:
        raise e
