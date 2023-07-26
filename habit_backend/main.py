from sqlmodel import create_engine, SQLModel
from fastapi import FastAPI

from app.service import HabitsTrackingService
from app.routers import create_user_routers, create_habit_routers, create_habit_event_routers
from app.exception_handler import add_exception_handler
from app.db.client import DatabaseClient
from app.config import Config


def create_habit_db_engine(config: Config):
    connect_args = {"check_same_thread": False}
    return create_engine(config.db_host, echo=True, connect_args=connect_args)


def create_database(engine) -> DatabaseClient:
    database = DatabaseClient(engine)
    return database


def reset_database(engine) -> None:
    SQLModel.metadata.drop_all()
    SQLModel.metadata.create_all()


def create_service(db_client: DatabaseClient) -> HabitsTrackingService:
    service = HabitsTrackingService(db_client)
    return service


def create_app(service: HabitsTrackingService):
    tags_metadata = [
        {
            "name": "user",
            "description": "Operations with users. The **login** logic is also here.",
        },
        {
            "name": "habit",
            "description": "Operation with the habits",
        },
        {
            "name": "habit_event",
            "description": "Operation with the habit_event",
        },
    ]

    fast_api = FastAPI(openapi_tags=tags_metadata)

    user_routers = create_user_routers(service)
    habit_routers = create_habit_routers(service)
    habit_event_router = create_habit_event_routers(service)

    fast_api.include_router(user_routers)
    fast_api.include_router(habit_routers)
    fast_api.include_router(habit_event_router)
    add_exception_handler(service=fast_api)

    return fast_api


habit_conf = Config()
habit_db_engine = create_habit_db_engine(habit_conf)
habit_db = create_database(habit_db_engine)
habit_service = create_service(habit_db)
app = create_app(habit_service)
