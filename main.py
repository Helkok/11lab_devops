from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from starlette.requests import Request

from middleware.middleware import DBSessionMiddleware
from user.routers import router as user_router
from auth.routers import router as auth_router
from utils import get_current_user

app = FastAPI()
app.add_middleware(DBSessionMiddleware)



@app.get("/")
async def root():
    return {"message": "Hello World"}

PROTECTED = [Depends(get_current_user)]
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router,dependencies=PROTECTED, prefix="/user", tags=["user"])


