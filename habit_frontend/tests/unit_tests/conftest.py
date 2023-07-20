import pytest

from htr.client.habit_tracker import HabitTrackerClient


@pytest.fixture
def mock_endpoint():
    return "http://www.habit-tracker.com"


@pytest.fixture
def valid_client(mock_endpoint):
    client = HabitTrackerClient(mock_endpoint)
    return client
