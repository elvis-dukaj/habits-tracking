from fastapi import FastAPI

from routers.routers import create_user_routers
from exception_handler import add_exception_handler


def create_service():
    fast_api = FastAPI()

    habits_routers = create_user_routers()

    fast_api.include_router(habits_routers)
    add_exception_handler(service=fast_api)

    return fast_api


service = create_service()
