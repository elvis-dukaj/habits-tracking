import pytest


@pytest.fixture(scope="session")
def valid_user_id() -> int:
    return 1
