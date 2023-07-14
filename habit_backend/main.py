from sqlmodel import create_engine, SQLModel
from fastapi import FastAPI

from app.service.habit_tracker import HabitsTrackingService
from app.routers.user import create_user_routers
from app.routers.habit import create_habit_routers
from app.routers.habit_event import create_habit_event_routers
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
    fast_api = FastAPI()

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
