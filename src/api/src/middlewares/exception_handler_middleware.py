from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as err:
            print(err)
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(err)
            )