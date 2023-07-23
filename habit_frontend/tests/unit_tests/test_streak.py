import pandas

from htr.schemas.habit_event import HabitEvent
from htr.analytics import calculate_record_streak, calculate_current_streak, transform_to_panda_dataframe


def test_transform_to_dataframe_first_and_last_should_be_added():
    events_json = [
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},  # 3
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-04"},  # 3 <
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-07"},  # 4 XXX
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-11"},  # 3
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-14"},  # 4 XXX
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-18"},  # 3
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-21"},  # 3
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-24"},  # 3
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]
    periodicity: int = 3

    expected_dataframe = pandas.DataFrame({
        "start date": [' 2023-01-01', '2023-01-11', '2023-01-18'],
        "end date": [' 2023-01-07', '2023-01-14', '2023-01-24'],
        "streak": [2, 1, 2]
    })

    dataframe = transform_to_panda_dataframe(events, periodicity)
    # assert dataframe == expected_dataframe
    start_date_col = (dataframe['start date'] == expected_dataframe['start date'])
    end_date_col = (dataframe['end date'] == expected_dataframe['end date'])
    streak_col = (dataframe['streak'] == expected_dataframe['streak'])
    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()


def test_transform_to_dataframe_first_should_be_added_last_not():
    events_json = [
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},  # 3
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-04"},  # 3 <
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-07"},  # 4 XXX
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-11"},  # 3
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-14"},  # 4 XXX
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-18"},  # 3
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-21"},  # 3
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-29"},  # 3
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]
    periodicity: int = 3

    expected_dataframe = pandas.DataFrame({
        "start date": [' 2023-01-01', '2023-01-11', '2023-01-18'],
        "end date": [' 2023-01-07', '2023-01-14', '2023-01-21'],
        "streak": [2, 1, 1]
    })

    dataframe = transform_to_panda_dataframe(events, periodicity)
    # assert dataframe == expected_dataframe
    start_date_col = (dataframe['start date'] == expected_dataframe['start date'])
    end_date_col = (dataframe['end date'] == expected_dataframe['end date'])
    streak_col = (dataframe['streak'] == expected_dataframe['streak'])
    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()


def test_transform_to_dataframe__should__not_add_first_and_last():
    events_json = [
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},  # XXX
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-10"},  # -->
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-13"},  # -
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-17"},  # <-- 2
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-25"},  # XXX
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-30"},  # XXX
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-02-10"},  # -->
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-02-12"},  # <-- 1
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-02-20"},  # 3
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]

    expected_dataframe = pandas.DataFrame({
        "start date": ['2023-01-10', '2023-02-10'],
        "end date": ['2023-01-13', '2023-02-12'],
        "streak": [1, 1]
    })

    periodicity: int = 3
    dataframe = transform_to_panda_dataframe(events, periodicity)
    start_date_col = (dataframe['start date'] == expected_dataframe['start date'])
    end_date_col = (dataframe['end date'] == expected_dataframe['end date'])
    streak_col = (dataframe['streak'] == expected_dataframe['streak'])

    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()


def test_all_streaks():
    events_json = [
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-02"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-03"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-04"},
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]

    expected_dataframe = pandas.DataFrame({
        "start date": ['2023-01-01'],
        "end date": ['2023-01-04'],
        "streak": [3]
    })

    periodicity: int = 1
    dataframe = transform_to_panda_dataframe(events, periodicity)
    start_date_col = (dataframe['start date'] == expected_dataframe['start date'])
    end_date_col = (dataframe['end date'] == expected_dataframe['end date'])
    streak_col = (dataframe['streak'] == expected_dataframe['streak'])

    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()



def test_no_streaks():
    events_json = [
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-01"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-03"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-05"},
        {"user_id": 1, "habit_id": 1, "completed_at": "2023-01-10"},
    ]

    events: list[HabitEvent] = [HabitEvent(**event_json) for event_json in events_json]

    expected_dataframe = pandas.DataFrame({
        "start date": [],
        "end date": [],
        "streak": []
    })

    periodicity: int = 1
    dataframe = transform_to_panda_dataframe(events, periodicity)
    start_date_col = (dataframe['start date'] == expected_dataframe['start date'])
    end_date_col = (dataframe['end date'] == expected_dataframe['end date'])
    streak_col = (dataframe['streak'] == expected_dataframe['streak'])

    assert start_date_col.all()
    assert end_date_col.all()
    assert streak_col.all()
