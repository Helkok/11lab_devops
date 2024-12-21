from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from db import async_session_maker


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with async_session_maker() as session:
            request.state.db = session
            response = await call_next(request)
        return response
