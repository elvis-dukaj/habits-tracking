from fastapi.testclient import TestClient

import pytest

from main import create_service


@pytest.fixture()
def mock_application():
    app = create_service()
    mock = TestClient(app)
    return mock
