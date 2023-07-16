
from app.schemas.habit import HabitRead


def test_habit_create_success(mock_application, habit_url, valid_user_id):
    habit_json_list = [
        {
            "user_id": valid_user_id,
            "task": "exercises for the back pain",
            "periodicity": 1
        },
        {
            "user_id": valid_user_id,
            "task": "do the exercises for the neck",
            "periodicity": 1
        },
        {
            "user_id": valid_user_id,
            "task": "bouldering",
            "periodicity": 3
        },
        {
            "user_id": valid_user_id,
            "task": "exercises fro the back pain",
            "periodicity": 1
        },
        {
            "user_id": valid_user_id,
            "task": "call my parents",
            "periodicity": 7
        },
    ]

    for json_body in habit_json_list:
        response = mock_application.post(url=habit_url, json=json_body)

        body = response.json()
        assert body is not None

        created_habit = HabitRead(**response.json())

        assert created_habit.habit_id is not None
        assert created_habit.user_id == 1
        assert created_habit.task == json_body["task"]
        assert created_habit.periodicity == json_body["periodicity"]
        assert response.status_code == 201


def test_get_habits_by_habit_id(mock_application, habit_by_id_url, valid_habit_id):
    response = mock_application.get(url=habit_by_id_url)

    json_body = response.json()
    assert json_body is not None

    habit = HabitRead(**json_body)

    assert habit.user_id == 1
    assert habit.habit_id == valid_habit_id
    assert response.status_code == 200


def test_get_habits_by_periodicity(mock_application, habit_by_periodicity_url, valid_periodicity):
    response = mock_application.get(url=habit_by_periodicity_url)

    json_body_list = response.json()

    for json_body in json_body_list:
        habit = HabitRead(**json_body)
        assert habit.periodicity == valid_periodicity

    assert response.status_code == 200


def test_can_delete_habits(mock_application, habit_url):
    habit_ids: list[int] = [1, 2, 3, 4, 5]

    for habit_id in habit_ids:
        url = f"{habit_url}/{habit_id}"
        response = mock_application.delete(url=url)

        assert response.status_code == 200
