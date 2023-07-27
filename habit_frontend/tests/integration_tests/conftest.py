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
def valid_user_created_at():
    return "2023-07-01"


@pytest.fixture
def valid_habit_id():
    return 200


@pytest.fixture
def valid_habit_task():
    return "test task"


@pytest.fixture
def valid_habit_created_at():
    return "2023-07-01"


@pytest.fixture
def valid_habit_event_completed_date():
    return "2023-07-24"


@pytest.fixture
def valid_habit_event_id():
    return 1000
