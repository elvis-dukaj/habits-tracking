import pytest

from app.schemas.user import UserRead, UserCreate


def test_user_create_success(mock_application, user_url, valid_user_id, valid_username, valid_user_email):
    json_body = {
        "username": valid_username,
        "email": valid_user_email
    }
    response = mock_application.post(url=user_url, json=json_body)

    body = response.json()
    assert body is not None

    created_user = UserRead(**response.json())

    assert created_user.user_id == valid_user_id
    assert created_user.username == json_body["username"]
    assert created_user.email == json_body["email"]
    assert response.status_code == 201


def test_get_user_by_username(mock_application, valid_user_by_username_url, valid_user_id, valid_username,
                              valid_user_email):
    response = mock_application.get(url=valid_user_by_username_url)
    selected_user = UserRead(**response.json())

    assert selected_user.user_id == valid_user_id
    assert selected_user.username == valid_username
    assert selected_user.email == valid_user_email
    assert response.status_code == 200


def test_get_user_by_user_id(mock_application, valid_user_by_user_id_url, valid_user_id, valid_username,
                             valid_user_email):
    response = mock_application.get(url=valid_user_by_user_id_url)
    selected_user = UserRead(**response.json())

    assert selected_user.user_id == valid_user_id
    assert selected_user.username == valid_username
    assert selected_user.email == valid_user_email
    assert response.status_code == 200

# def test_user_can_be_deleted(mock_application, valid_delete_by_user_id, valid_user_by_user_id_url):
#     response = mock_application.delete(url=valid_delete_by_user_id)
#     assert response.status_code == 200
#
#     response = mock_application.get(url=valid_user_by_user_id_url)
#     assert response.status_code != 200
#
#
# def test_get_invalid_username_returns_error(mock_application, invalid_user_by_username_url):
#     response = mock_application.get(url=invalid_user_by_username_url)
#     assert response.status_code == 404
#
#
# def test_get_delete_invalid_user_is_handled(mock_application, invalid_user_by_user_id_url):
#     response = mock_application.get(url=invalid_user_by_user_id_url)
#     assert response.status_code == 404
