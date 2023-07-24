from click.testing import CliRunner
import responses

from htr.cli import cli


@responses.activate
def test_user_create_success(mock_endpoint):
    username = "test_user"
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

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'user', 'create', '--username', username])

    assert f"User {username} created with id: {expected_user_id}" in res.output
