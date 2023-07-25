import pandas
from click.testing import CliRunner
import responses
from tabulate import tabulate
import plotext as plot

from htr.cli import cli


@responses.activate
def test_habit_can_create(mock_endpoint, valid_userid, valid_habit_task, valid_habit_id):
    expected_periodicity: int = 3

    responses.post(
        url=f"{mock_endpoint}/habit",
        json={
            "task": valid_habit_task,
            "user_id": valid_userid,
            "periodicity": expected_periodicity,
            "habit_id": valid_habit_id
        },
        status=201
    )

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'habit', '--user-id', valid_userid, 'create', '--task',
                              valid_habit_task, "--periodicity", expected_periodicity])

    assert f"Habit {valid_habit_task} created with id {valid_habit_id}" in res.output


@responses.activate
def test_habit_can_list_all_habits(mock_endpoint, valid_userid):
    json_body = []

    for habit_id in range(10):
        json_body.append({
            "user_id": 1,
            "habit_id": habit_id,
            "task": f"task {habit_id}",
            "periodicity": 1,
        })

    for habit_id in range(10, 20):
        json_body.append({
            "user_id": 1,
            "habit_id": habit_id,
            "task": f"task {habit_id}",
            "periodicity": 3,
        })

    for habit_id in range(20, 30):
        json_body.append({
            "user_id": 1,
            "habit_id": habit_id,
            "task": f"task {habit_id}",
            "periodicity": 5,
        })

    responses.get(
        url=f"{mock_endpoint}/habit/?user_id={valid_userid}&offset=0&limit=100",
        json=json_body,
        status=200
    )

    df = pandas.DataFrame(json_body)

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'habit', '--user-id', valid_userid, 'list'])

    assert tabulate(df, headers='keys', tablefmt='psql') in res.output


@responses.activate
def test_habit_can_be_deleted(mock_endpoint, valid_userid, valid_habit_id):
    responses.delete(url=f"{mock_endpoint}/habit/{valid_habit_id}")

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'habit', '--user-id', valid_userid, 'delete', '--habit-id',
                              valid_habit_id])

    assert f"Habit '{valid_habit_id}' deleted" in res.output
