from fastapi import FastAPI

from routers.routers import create_user_routers


def create_service():
    fast_api = FastAPI()

    habits_routers = create_user_routers()

    fast_api.include_router(habits_routers)

    return fast_api


service = create_service()
