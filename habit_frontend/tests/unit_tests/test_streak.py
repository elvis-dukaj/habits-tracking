import pandas

from htr.schemas.habit_event import HabitEvent
from htr.analytics import transform_to_panda_dataframe


def test_transform_to_dataframe_first_and_last_should_be_added():
    events_json = [
        {"habit_event_id": 0, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},  # 3
        {"habit_event_id": 1, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-04"},  # 3 <
        {"habit_event_id": 2, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-07"},  # 4 XXX
        {"habit_event_id": 3, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-11"},  # 3
        {"habit_event_id": 4, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-14"},  # 4 XXX
        {"habit_event_id": 5, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-18"},  # 3
        {"habit_event_id": 6, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-21"},  # 3
        {"habit_event_id": 7, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-24"},  # 3
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]
    periodicity: int = 3

    expected_dataframe = pandas.DataFrame({
        "Start Date": [' 2023-01-01', '2023-01-11', '2023-01-18'],
        "End Date": [' 2023-01-07', '2023-01-14', '2023-01-24'],
        "Streak": [2, 1, 2]
    })

    dataframe = transform_to_panda_dataframe(events, periodicity)
    # assert dataframe == expected_dataframe
    start_date_col = (dataframe['Start Date'] == expected_dataframe['Start Date'])
    end_date_col = (dataframe['End Date'] == expected_dataframe['End Date'])
    streak_col = (dataframe['Streak'] == expected_dataframe['Streak'])
    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()


def test_transform_to_dataframe_first_should_be_added_last_not():
    events_json = [
        {"habit_event_id": 0, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},  # 3
        {"habit_event_id": 1, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-04"},  # 3 <
        {"habit_event_id": 2, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-07"},  # 4 XXX
        {"habit_event_id": 3, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-11"},  # 3
        {"habit_event_id": 4, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-14"},  # 4 XXX
        {"habit_event_id": 5, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-18"},  # 3
        {"habit_event_id": 6, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-21"},  # 3
        {"habit_event_id": 7, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-29"},  # 3
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]
    periodicity: int = 3

    expected_dataframe = pandas.DataFrame({
        "Start Date": [' 2023-01-01', '2023-01-11', '2023-01-18'],
        "End Date": [' 2023-01-07', '2023-01-14', '2023-01-21'],
        "Streak": [2, 1, 1]
    })

    dataframe = transform_to_panda_dataframe(events, periodicity)
    # assert dataframe == expected_dataframe
    start_date_col = (dataframe['Start Date'] == expected_dataframe['Start Date'])
    end_date_col = (dataframe['End Date'] == expected_dataframe['End Date'])
    streak_col = (dataframe['Streak'] == expected_dataframe['Streak'])
    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()


def test_transform_to_dataframe__should__not_add_first_and_last():
    events_json = [
        {"habit_event_id": 0, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},  # XXX
        {"habit_event_id": 1, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-10"},  # -->
        {"habit_event_id": 2, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-13"},  # -
        {"habit_event_id": 3, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-17"},  # <-- 2
        {"habit_event_id": 4, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-25"},  # XXX
        {"habit_event_id": 5, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-30"},  # XXX
        {"habit_event_id": 6, "user_id": 1, "habit_id": 1, "completed_at": "2023-02-10"},  # -->
        {"habit_event_id": 7, "user_id": 1, "habit_id": 1, "completed_at": "2023-02-12"},  # <-- 1
        {"habit_event_id": 8, "user_id": 1, "habit_id": 1, "completed_at": "2023-02-20"},  # 3
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]

    expected_dataframe = pandas.DataFrame({
        "Start Date": ['2023-01-10', '2023-02-10'],
        "End Date": ['2023-01-13', '2023-02-12'],
        "Streak": [1, 1]
    })

    periodicity: int = 3
    dataframe = transform_to_panda_dataframe(events, periodicity)
    start_date_col = (dataframe['Start Date'] == expected_dataframe['Start Date'])
    end_date_col = (dataframe['End Date'] == expected_dataframe['End Date'])
    streak_col = (dataframe['Streak'] == expected_dataframe['Streak'])

    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()


def test_all_streaks():
    events_json = [
        {"habit_event_id": 0, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},
        {"habit_event_id": 1, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-02"},
        {"habit_event_id": 2, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-03"},
        {"habit_event_id": 3, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-04"},
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]

    expected_dataframe = pandas.DataFrame({
        "Start Date": ['2023-01-01'],
        "End Date": ['2023-01-04'],
        "Streak": [3]
    })

    periodicity: int = 1
    dataframe = transform_to_panda_dataframe(events, periodicity)
    start_date_col = (dataframe['Start Date'] == expected_dataframe['Start Date'])
    end_date_col = (dataframe['End Date'] == expected_dataframe['End Date'])
    streak_col = (dataframe['Streak'] == expected_dataframe['Streak'])

    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()


def test_no_streaks():
    events_json = [
        {"habit_event_id": 0, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},
        {"habit_event_id": 1, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-03"},
        {"habit_event_id": 2, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-05"},
        {"habit_event_id": 3, "user_id": 1, "habit_id": 1, "completed_at": "2023-01-10"},
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]

    expected_dataframe = pandas.DataFrame({
        "Start Date": [],
        "End Date": [],
        "Streak": []
    })

    periodicity: int = 1
    dataframe = transform_to_panda_dataframe(events, periodicity)
    start_date_col = (dataframe['Start Date'] == expected_dataframe['Start Date'])
    end_date_col = (dataframe['End Date'] == expected_dataframe['End Date'])
    streak_col = (dataframe['Streak'] == expected_dataframe['Streak'])

    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()


def test_no_events():
    events_json = []

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]

    expected_dataframe = pandas.DataFrame({
        "Start Date": [],
        "End Date": [],
        "Streak": []
    })

    periodicity: int = 1
    dataframe = transform_to_panda_dataframe(events, periodicity)
    start_date_col = (dataframe['Start Date'] == expected_dataframe['Start Date'])
    end_date_col = (dataframe['End Date'] == expected_dataframe['End Date'])
    streak_col = (dataframe['Streak'] == expected_dataframe['Streak'])

    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()
