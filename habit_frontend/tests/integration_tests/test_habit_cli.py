import pandas
from click.testing import CliRunner
import responses
from tabulate import tabulate

from htr.cli import cli
from htr.analytics import tabulate_dataframe


@responses.activate
def test_habit_can_create(mock_endpoint, valid_userid, valid_habit_task, valid_habit_id, valid_habit_event_id,
                          valid_habit_created_at):
    expected_periodicity: int = 3

    responses.post(
        url=f"{mock_endpoint}/habit",
        json={
            "task": valid_habit_task,
            "user_id": valid_userid,
            "periodicity": expected_periodicity,
            "habit_id": valid_habit_id,
            "created_at": valid_habit_created_at
        },
        status=201
    )

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'habit', '--user-id', valid_userid, 'create', '--task',
                              valid_habit_task, "--periodicity", expected_periodicity, "--date",
                              valid_habit_created_at])

    assert f"Habit '{valid_habit_task}' created with id {valid_habit_id}" in res.output


@responses.activate
def test_habit_can_list_all_habits(mock_endpoint, valid_userid, valid_habit_created_at):
    json_body = []

    for habit_id in range(10):
        json_body.append({
            "user_id": 1,
            "habit_id": habit_id,
            "task": f"task {habit_id}",
            "periodicity": 1,
            "created_at": valid_habit_created_at
        })

    for habit_id in range(10, 20):
        json_body.append({
            "user_id": 1,
            "habit_id": habit_id,
            "task": f"task {habit_id}",
            "periodicity": 3,
            "created_at": valid_habit_created_at
        })

    for habit_id in range(20, 30):
        json_body.append({
            "user_id": 1,
            "habit_id": habit_id,
            "task": f"task {habit_id}",
            "periodicity": 5,
            "created_at": valid_habit_created_at
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
def test_habit_can_list_habits_by_periodicity(mock_endpoint, valid_userid, valid_habit_created_at):
    habits_with_periodicity_1_json: list = []

    for habit_id in range(10):
        habits_with_periodicity_1_json.append({
            "user_id": 1,
            "habit_id": habit_id,
            "task": f"task {habit_id}",
            "periodicity": 1,
            "created_at": valid_habit_created_at
        })

    responses.get(
        url=f"{mock_endpoint}/habit/?user_id={valid_userid}&offset=0&limit=100&periodicity=1",
        json=habits_with_periodicity_1_json,
        status=200
    )

    df = pandas.DataFrame(habits_with_periodicity_1_json)

    runner = CliRunner()
    res = runner.invoke(cli, [
        '--endpoint', mock_endpoint, 'habit', '--user-id', valid_userid, 'list', '--with-periodicity', 1
    ])

    assert tabulate(df, headers='keys', tablefmt='psql') in res.output


@responses.activate
def test_habit_can_be_deleted(mock_endpoint, valid_userid, valid_habit_id):
    responses.delete(url=f"{mock_endpoint}/habit/{valid_habit_id}")

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'habit', '--user-id', valid_userid, 'delete', '--habit-id',
                              valid_habit_id])

    assert f"Habit '{valid_habit_id}' deleted" in res.output


@responses.activate
def test_habit_can_be_marked_as_complete(mock_endpoint, valid_userid, valid_habit_id, valid_habit_event_id,
                                         valid_habit_event_completed_date, valid_habit_task, valid_habit_created_at):
    responses.post(
        url=f"{mock_endpoint}/habit_event",
        json={
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": valid_habit_event_completed_date,
            "habit_event_id": valid_habit_event_id
        },
        status=201
    )
    responses.get(
        url=f"{mock_endpoint}/habit/{valid_habit_id}",
        json={
            "user_id": valid_userid,
            "task": valid_habit_task,
            "periodicity": 3,
            "habit_id": valid_habit_id,
            "created_at": valid_habit_created_at
        }
    )

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'habit', '--user-id', valid_userid, 'complete', '--habit-id',
                              valid_habit_id, '--completed-date', valid_habit_event_completed_date])

    assert f"Habit '{valid_habit_task}' completed" in res.output


@responses.activate
def test_habit_can_show_history(mock_endpoint, valid_userid, valid_habit_id, valid_habit_event_id,
                                valid_habit_event_completed_date, valid_habit_task, valid_habit_created_at):
    habit_json = {
        "user_id": valid_userid,
        "task": valid_habit_task,
        "periodicity": 1,
        "habit_id": valid_habit_id,
        "created_at": valid_habit_created_at
    }

    responses.get(
        url=f"{mock_endpoint}/habit/{valid_habit_id}",
        json=habit_json
    )

    habit_events_json = [
        {
            "habit_event_id": 1,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-18"
        },
        {
            "habit_event_id": 2,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-19"
        },
        {
            "habit_event_id": 3,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-20"
        },
        {
            "habit_event_id": 4,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-21"
        },
        {
            "habit_event_id": 5,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-30"
        },
        {
            "habit_event_id": 6,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-31"
        }
    ]

    responses.get(
        url=f"{mock_endpoint}/habit_event/?user_id={valid_userid}&offset=0&limit=100&habit_id={valid_habit_id}",
        json=habit_events_json
    )

    runner = CliRunner()
    res = runner.invoke(
        cli, [
            '--endpoint', mock_endpoint,
            'habit', '--user-id', valid_userid,
            'history', '--habit-id', valid_habit_id
        ]
    )

    df = pandas.DataFrame({
        "Start Date": ["2023-07-18 00:00:00", "2023-07-30 00:00:00"],
        "End Date": ["2023-07-21 00:00:00", "2023-07-31 00:00:00"],
        "Streak": [3, 1],
    })

    assert tabulate_dataframe(df) in res.output


@responses.activate
def test_habit_can_show_statistic(mock_endpoint, valid_userid, valid_habit_id, valid_habit_event_id,
                                  valid_habit_event_completed_date, valid_habit_task, valid_habit_created_at):
    habit_json = {
        "user_id": valid_userid,
        "task": valid_habit_task,
        "periodicity": 1,
        "habit_id": valid_habit_id,
        "created_at": valid_habit_created_at
    }

    responses.get(
        url=f"{mock_endpoint}/habit/{valid_habit_id}",
        json=habit_json
    )

    habit_events_json = [
        {
            "habit_event_id": 1,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-18"
        },
        {
            "habit_event_id": 2,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-19"
        },
        {
            "habit_event_id": 3,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-20"
        },
        {
            "habit_event_id": 4,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-21"
        },
        {
            "habit_event_id": 5,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-30"
        },
        {
            "habit_event_id": 6,
            "user_id": valid_userid,
            "habit_id": valid_habit_id,
            "completed_at": "2023-07-31"
        }
    ]

    responses.get(
        url=f"{mock_endpoint}/habit_event/?user_id={valid_userid}&offset=0&limit=100&habit_id={valid_habit_id}",
        json=habit_events_json
    )

    runner = CliRunner()
    res = runner.invoke(
        cli, [
            '--endpoint', mock_endpoint,
            'habit', '--user-id', valid_userid,
            'statistic', '--habit-id', valid_habit_id
        ]
    )

    df = pandas.DataFrame({
        "Longest": [3],
        "Last": [1],
        "Median": [2],
        "Mean": [2],
        "Total Streaks": [4],
        "Expected Streaks": [13],
        "Score": [0.307692]
    })

    assert tabulate_dataframe(df) in res.output
