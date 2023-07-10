import pytest

from app.schemas.user import User
from app.exception import UserNotFoundError


def create_valid_user() -> dict:
    json = {
        "username": "olta",
        "email": "olta",
        "user_id": None,
        "created_at": None,
    }
    return json


def test_user_create_success(mock_application, user_url):
    user_data = create_valid_user()
    response = mock_application.post(url=user_url, json=user_data)

    body = response.json()
    assert body is not None

    create_user = User(**response.json())

    assert create_user.username == 'olta'
    assert create_user.email == 'olta'
    assert create_user.user_id is not None
    assert create_user.user_id != 0
    assert response.status_code == 201


def test_get_user_by_username(mock_application, user_url):
    user_data = create_valid_user()
    response = mock_application.post(url=user_url, json=user_data)

    response = mock_application.get(url=f"{user_url}/get_by_username/olta")
    olta_user = User(**response.json())

    assert response.status_code == 200
    assert olta_user.username == "olta"
    assert olta_user.email == "olta"
    assert olta_user.user_id is not None


def test_get_user_by_user_id(mock_application, user_url):
    user_data = create_valid_user()
    response = mock_application.post(url=user_url, json=user_data)

    response = mock_application.get(url=f"{user_url}/get_by_username/olta")
    olta_user = User(**response.json())

    user_id = olta_user.user_id

    response = mock_application.get(url=f"{user_url}/get_by_id/{user_id}")
    olta_user = User(**response.json())

    assert response.status_code == 200
    assert olta_user.username == "olta"
    assert olta_user.email == "olta"
    assert olta_user.user_id == user_id


def test_user_can_be_deleted(mock_application, user_url):
    user_data = create_valid_user()
    response = mock_application.post(url=user_url, json=user_data)

    response = mock_application.get(url=f"{user_url}/get_by_username/olta")
    olta_user = User(**response.json())

    user_id = olta_user.user_id

    response = mock_application.delete(url=f"{user_url}/{user_id}")

    assert response.status_code == 200


def test_get_invalid_username_returns_error(mock_application, user_url):
    response = mock_application.get(url=f"{user_url}/get_by_username/olta")
    assert response.status_code == 404


def test_get_delete_invalid_user_is_handled(mock_application, user_url):
    response = mock_application.get(url=f"{user_url}/get_by_id/100")
    assert response.status_code == 404
