from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from .errors import SpbBaseException


def add_handler(app: FastAPI):
    @app.exception_handler(SpbBaseException)
    async def handler(request: Request, exc: SpbBaseException):
        return JSONResponse(
            status_code=exc.HTTP_CODE,
            content={"detail": exc.message},
        )
