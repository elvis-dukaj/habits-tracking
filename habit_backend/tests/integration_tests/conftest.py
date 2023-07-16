from typing import Type
import pytest

from sqlmodel import create_engine, SQLModel
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import create_service, create_app
from app.config import Config
from app.schemas.user import User
from app.db.client import DatabaseClient


@pytest.fixture(scope="session")
def mock_configuration() -> Type[Config]:
    config = Config
    config.db_host = "sqlite://"
    return config


@pytest.fixture(scope="session")
def mock_database(mock_configuration):
    engine = create_engine(mock_configuration.db_host, echo=False, connect_args={'check_same_thread': False},
                           poolclass=StaticPool)

    # clear all the tables and regenerate them
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    database = DatabaseClient(engine)

    return database


@pytest.fixture
def mock_application(mock_database):
    service = create_service(mock_database)
    app = create_app(service)
    mock = TestClient(app)
    return mock


@pytest.fixture
def valid_user_id():
    return 1


@pytest.fixture
def valid_username():
    return "olta"


@pytest.fixture
def invalid_user_id():
    return 100000


@pytest.fixture
def invalid_username():
    return "i_dont_exists"


@pytest.fixture
def user_url():
    return "/user"


@pytest.fixture
def valid_user_by_username_url(user_url, valid_username):
    return f"{user_url}/get_by_username/{valid_username}"


@pytest.fixture
def valid_user_by_user_id_url(user_url, valid_user_id):
    return f"{user_url}/get_by_id/{valid_user_id}"


@pytest.fixture
def valid_delete_by_user_id(user_url, valid_user_id):
    return f"{user_url}/{valid_user_id}"


@pytest.fixture
def invalid_user_by_user_id_url(user_url, invalid_user_id):
    return f"{user_url}/get_by_id/{invalid_user_id}"


@pytest.fixture
def invalid_user_by_username_url(user_url, invalid_username):
    return f"{user_url}/get_by_username/{invalid_username}"


@pytest.fixture
def valid_habit_id():
    return 1


@pytest.fixture
def valid_periodicity():
    return 3


@pytest.fixture
def valid_habit_event_id():
    return 1


@pytest.fixture
def habit_url():
    return "/habit"


@pytest.fixture
def habit_by_id_url(habit_url, valid_habit_id):
    return f"{habit_url}/{valid_habit_id}"


@pytest.fixture
def valid_habit_by_user_id_url(habit_url, valid_user_id):
    return f"{habit_url}/?user_id={valid_user_id}"


@pytest.fixture
def habit_by_periodicity_url(habit_url, valid_periodicity):
    return f"{habit_url}/by_periodicity/{valid_periodicity}"


@pytest.fixture
def habit_event_url():
    return f"/habit_event"


@pytest.fixture
def habit_event_get_by_id_url(habit_event_url, valid_habit_event_id):
    return f"{habit_event_url}/id/{valid_habit_event_id}"


@pytest.fixture
def habit_event_by_user_url(habit_event_url, valid_user_id, valid_habit_id):
    return f"{habit_event_url}/{valid_user_id}"


@pytest.fixture
def habit_event_by_user_and_habit_id_url(habit_event_url, valid_user_id, valid_habit_id):
    return f"{habit_event_url}/{valid_user_id}/{valid_habit_id}"
