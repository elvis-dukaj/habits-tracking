from typing import Type
import pytest

from fastapi.testclient import TestClient

from main import create_service, create_app
from app.config import Config
from app.schemas.user import User
from app.db.client import DatabaseClient
from models.create_tables import create_tables, drop_tables


@pytest.fixture
def mock_configuration() -> Type[Config]:
    config = Config
    config.db_host = "test.db"
    return config


@pytest.fixture
def mock_database(mock_configuration):
    database = DatabaseClient(mock_configuration.db_host)
    cur = database._cursor

    drop_tables(cur)
    create_tables(cur)

    return database


@pytest.fixture
def mock_application(mock_database):
    service = create_service(mock_database)
    app = create_app(service)
    mock = TestClient(app)
    return mock


@pytest.fixture
def user_url():
    return "/user"


@pytest.fixture
def valid_user_id():
    return 1


@pytest.fixture
def valid_username():
    return "olta"


@pytest.fixture
def valid_user_email():
    return "olta"


@pytest.fixture
def valid_user(valid_user_id, valid_username, valid_user_email):
    user = User(
        user_id=valid_user_id,
        username=valid_username,
        email=valid_user_email
    )
    return user


@pytest.fixture
def valid_user_by_username_url(user_url, valid_username):
    return f"{user_url}/get_by_username/{valid_username}"
