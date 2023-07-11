import pytest

from app.schemas.user import User
from app.exception import UserNotFoundError


def test_user_create_success(mock_application, user_url, valid_user):
    response = mock_application.post(url=user_url, json=dict(valid_user))

    body = response.json()
    assert body is not None

    create_user = User(**response.json())

    assert create_user.user_id == valid_user.user_id
    assert create_user.username == valid_user.username
    assert create_user.email == valid_user.email

    assert response.status_code == 201


def test_get_user_by_username(mock_application, valid_user_by_username_url, valid_user):
    response = mock_application.get(url=valid_user_by_username_url)
    olta_user = User(**response.json())

    assert olta_user.user_id == valid_user.user_id
    assert olta_user.username == valid_user.username
    assert olta_user.email == valid_user.email
    assert response.status_code == 200


def test_get_user_by_user_id(mock_application, valid_user_by_user_id_url, valid_user):
    response = mock_application.get(url=valid_user_by_user_id_url)
    olta_user = User(**response.json())

    assert response.status_code == 200
    assert olta_user.username == valid_user.username
    assert olta_user.email == valid_user.email
    assert olta_user.user_id == valid_user.user_id


def test_user_can_be_deleted(mock_application, valid_delete_by_user_id, valid_user_by_user_id_url):
    response = mock_application.delete(url=valid_delete_by_user_id)
    assert response.status_code == 200

    response = mock_application.get(url=valid_user_by_user_id_url)
    assert response.status_code != 200


def test_get_invalid_username_returns_error(mock_application, invalid_user_by_username_url):
    response = mock_application.get(url=invalid_user_by_username_url)
    assert response.status_code == 404


def test_get_delete_invalid_user_is_handled(mock_application, invalid_user_by_user_id_url):
    response = mock_application.get(url=invalid_user_by_user_id_url)
    assert response.status_code == 404
