from click.testing import CliRunner
import responses

from htr.cli import cli


@responses.activate
def test_user_can_create(mock_endpoint, valid_username, valid_userid):
    responses.post(
        url=f"{mock_endpoint}/user",
        json={
            "username": valid_username,
            "user_id": valid_userid,
        },
        status=201
    )

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'user', 'create', '--username', valid_username])

    assert f"User {valid_username} created with id: {valid_userid}" in res.output


@responses.activate
def test_user_can_login(mock_endpoint, valid_username, valid_userid):
    resp = responses.get(
        url=f"{mock_endpoint}/user/username/{valid_username}",
        json={
            "username": valid_username,
            "user_id": valid_userid,
        },
    )

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'user', 'login', '--username', valid_username])

    assert f"User {valid_username} has user_id {valid_userid}" in res.output


@responses.activate
def test_user_can_delete(mock_endpoint, valid_userid):
    resp = responses.delete(
        url=f"{mock_endpoint}/user/{valid_userid}",
    )

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'user', 'delete', '--user-id', valid_userid])

    assert f"User {valid_userid} deleted" in res.output
