import pytest

from app.schemas.user import User


@pytest.fixture(scope="session")
def valid_user_id() -> int:
    return 1
