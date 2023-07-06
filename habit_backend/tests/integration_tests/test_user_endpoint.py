def test_user_create_success(mock_application):
    json = {
        "username": "olta",
        "email": "olta"
    }

    response = mock_application.post(url=f"/user", json=json)
    assert response.status_code == 201
