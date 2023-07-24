import pytest


@pytest.fixture
def mock_endpoint():
    return "http://www.htr.com"


@pytest.fixture
def valid_username():
    return "test_user"


@pytest.fixture
def valid_userid():
    return 100


@pytest.fixture
def valid_habit_id():
    return 200


@pytest.fixture
def valid_habit_task():
    return "test task"
