from fastapi import FastAPI

from service.habit import HabitsTrackingService
from routers.user import create_user_routers
from routers.habit import create_habit_routers
from exception_handler import add_exception_handler
from db.client import DatabaseClient


def create_service():
    fast_api = FastAPI()

    database = DatabaseClient()
    habit_service = HabitsTrackingService(database)

    user_routers = create_user_routers(habit_service)
    habit_routers = create_habit_routers(habit_service)

    fast_api.include_router(user_routers)
    fast_api.include_router(habit_routers)
    add_exception_handler(service=fast_api)

    return fast_api


service = create_service()
