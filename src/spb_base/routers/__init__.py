from fastapi import FastAPI

from . import item


def include_routers(app: FastAPI):
    app.include_router(item.router)
