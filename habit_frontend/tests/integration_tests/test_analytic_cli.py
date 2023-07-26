import pandas
from click.testing import CliRunner
import responses
from tabulate import tabulate

from htr.cli import cli
from htr.schemas import Habit, HabitEvent
from htr.analytics import tabulate_dataframe


@responses.activate
def test_can_calculate_statistics(mock_endpoint, valid_userid):
    habits_id = [1, 2, 3, 10, 11, 12, 13]
    habits_task = [
        "doing yoga in the morning",
        "learn German",
        "call my granny",
        "stretching",
        "clean the flat",
        "reading a book",
        "walk for 2km"
    ]
    habits_periodicities = [1, 1, 7, 1, 7, 1, 1]

    habits_json = []
    for habit_id, task, periodicity in zip(habits_id, habits_task, habits_periodicities):
        habits_json.append(
            {
                "user_id": valid_userid,
                "habit_id": habit_id,
                "task": task,
                "periodicity": periodicity,
            }
        )

    responses.get(
        url=f"{mock_endpoint}/habit/?user_id={valid_userid}&offset=0&limit=100",
        json=habits_json,
    )

    habit_event_index: int = 0
    habit_events = [
        [  # doing yoga in the morning
            "2023-01-20",
            "2023-01-21",
            "2023-01-22",
            "2023-01-23",  # 3 streaks
            "2023-02-01",
            "2023-02-02",  # 2 streaks
            "2023-02-01",
            "2023-03-01",
            "2023-03-02",  # 1 current streak
        ],
        [  # learn German
            "2023-07-20",
            "2023-07-21",  # 1 streaks
        ],  # call my granny
        [
            "2023-07-01",
        ],  # stretching
        [
            "2023-07-20",
            "2023-07-21",
            "2023-07-22"
        ],  # clean the flat
        [
            "2023-01-01",
            "2023-02-01",
            "2023-03-01",
            "2023-04-01",
            "2023-05-01",
        ],
        [],  # reading a book
        [],  # walk for 2km
    ]

    for habit_id, completed_dates in zip(habits_id, habit_events):
        events_json = []
        for completed_date in completed_dates:
            events_json.append({
                "habit_event_id": habit_event_index,
                "user_id": valid_userid,
                "habit_id": habit_id,
                "completed_at": completed_date
            })
            habit_event_index += 1

        responses.get(
            url=f"{mock_endpoint}/habit_event/?user_id={valid_userid}&offset=0&limit=100&habit_id={habit_id}",
            json=events_json
        )

    expected_last_streaks = [1, 1, 0, 2, 0, 0, 0]
    expected_longest_streaks = [3, 1, 0, 2, 0, 0, 0]
    expected_mean_streaks = [2, 1, 0, 2, 0, 0, 0]
    expected_expected_streak = [41, 1, 0, 2, 17, 0, 0]
    expected_streaka = [0.146341, 1, 0, 1, 0, 0, 0]

    expected_dataframe = pandas.DataFrame({
        "Habit ID": habits_id,
        "Task": habits_task,
        "Periodicity": habits_periodicities,
        "Last Streak": expected_last_streaks,
        "Longest Streak": expected_longest_streaks,
        "Average Streak": expected_mean_streaks,
        "Expected Streaks": expected_expected_streak,
        "Score": expected_streaka,
    })

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'statistic', '--user-id', valid_userid, 'view'])

    assert tabulate_dataframe(expected_dataframe) in res.output


@responses.activate
def test_habit_can_list_habits_by_periodicity(mock_endpoint, valid_userid):
    habits_with_periodicity_1_json: list = []

    for habit_id in range(10):
        habits_with_periodicity_1_json.append({
            "user_id": 1,
            "habit_id": habit_id,
            "task": f"task {habit_id}",
            "periodicity": 1,
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
                                         valid_habit_event_completed_date, valid_habit_task):
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
            "habit_id": valid_habit_id
        }
    )

    runner = CliRunner()
    res = runner.invoke(cli, ['--endpoint', mock_endpoint, 'habit', '--user-id', valid_userid, 'complete', '--habit-id',
                              valid_habit_id, '--completed-date', valid_habit_event_completed_date])

    assert f"Habit '{valid_habit_task}' completed" in res.output


@responses.activate
def test_habit_can_view(mock_endpoint, valid_userid, valid_habit_id, valid_habit_event_id,
                        valid_habit_event_completed_date, valid_habit_task):
    habit_json = {
        "user_id": valid_userid,
        "task": valid_habit_task,
        "periodicity": 1,
        "habit_id": valid_habit_id
    }

    responses.get(
        url=f"{mock_endpoint}/habit/{valid_habit_id}",
        json=habit_json
    )

    runner = CliRunner()
    res = runner.invoke(
        cli, [
            '--endpoint', mock_endpoint,
            'habit', '--user-id', valid_userid,
            'view', '--habit-id', valid_habit_id
        ]
    )

    habit = Habit(**habit_json)
    assert tabulate(habit) in res.output


@responses.activate
def test_habit_can_show_history(mock_endpoint, valid_userid, valid_habit_id, valid_habit_event_id,
                                valid_habit_event_completed_date, valid_habit_task):
    habit_json = {
        "user_id": valid_userid,
        "task": valid_habit_task,
        "periodicity": 1,
        "habit_id": valid_habit_id
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
        "start date": ["2023-07-18 00:00:00", "2023-07-30 00:00:00"],
        "end date": ["2023-07-21 00:00:00", "2023-07-31 00:00:00"],
        "streak": [3, 1],
    })

    assert tabulate_dataframe(df) in res.output


@responses.activate
def test_habit_can_show_statistic(mock_endpoint, valid_userid, valid_habit_id, valid_habit_event_id,
                                  valid_habit_event_completed_date, valid_habit_task):
    habit_json = {
        "user_id": valid_userid,
        "task": valid_habit_task,
        "periodicity": 1,
        "habit_id": valid_habit_id
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
        "Total Streaks": [4]
    })

    assert tabulate_dataframe(df) in res.output
