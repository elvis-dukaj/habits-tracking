import pytest
import responses


@responses.activate
def test_user_create_success(valid_client, mock_endpoint):
    username = "edukaj"
    expected_user_id = 100

    resp = responses.Response(
        method="POST",
        url=f"{mock_endpoint}/user",
        json={
            "username": username,
            "user_id": expected_user_id,
        },
        status=201
    )
    responses.add(resp)

    user_id: int = valid_client.add_user(username)
    assert user_id == expected_user_id
