import sqlite3

from fastapi import FastAPI

from app.service.habit_tracker import HabitsTrackingService
from app.routers.user import create_user_routers
from app.routers.habit import create_habit_routers
from app.routers.habit_event import create_habit_event_routers
from app.exception_handler import add_exception_handler
from app.db.client import DatabaseClient
from app.config import Config


def create_database(config: Config) -> DatabaseClient:
    database = DatabaseClient(config.db_host)
    return database


def create_service(db_client: DatabaseClient) -> HabitsTrackingService:
    habit_service = HabitsTrackingService(db_client)
    return habit_service


def create_app(service: HabitsTrackingService):
    fast_api = FastAPI()

    user_routers = create_user_routers(service)
    habit_routers = create_habit_routers(service)
    habit_event_router = create_habit_event_routers(service)

    fast_api.include_router(user_routers)
    fast_api.include_router(habit_routers)
    fast_api.include_router(habit_event_router)
    add_exception_handler(service=fast_api)

    # create_tables()

    return fast_api


conf = Config()
service = create_service(conf)
