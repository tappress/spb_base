from fastapi import FastAPI

from . import handlers


def add_exception_handlers(app: FastAPI) -> None:
    handlers.add_handler(app)
