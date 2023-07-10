from typing import Type
import pytest

from fastapi.testclient import TestClient

from main import create_service, create_app
from app.config import Config
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
