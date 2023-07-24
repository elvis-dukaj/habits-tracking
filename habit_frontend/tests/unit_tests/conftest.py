import pytest

from htr.client.habit_tracker import HabitTrackerClient


@pytest.fixture
def valid_client(mock_endpoint):
    client = HabitTrackerClient(mock_endpoint)
    return client
